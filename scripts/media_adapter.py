"""Deterministic media operations with explicit inputs and optional engines."""
import io
import json
import re
import tempfile
import unicodedata
from pathlib import Path

from adapter_io import integer, number, source, installed_path, process, write_json, runtime


def load_image(path):
    from PIL import Image, ImageOps
    data = runtime.read_limited(path)
    with Image.open(io.BytesIO(data)) as image:
        if image.width * image.height > 16_000_000 or getattr(image, 'n_frames', 1) != 1:
            raise ValueError('Use still images up to 16 million pixels')
        image.load()
        return ImageOps.exif_transpose(image).convert('RGBA')


def fitted(image, size):
    from PIL import Image, ImageOps
    canvas = Image.new('RGBA', size)
    small = ImageOps.contain(image, size, Image.Resampling.LANCZOS)
    canvas.alpha_composite(small, ((size[0] - small.width) // 2, (size[1] - small.height) // 2))
    return canvas


def enhance(root, job, out):
    from PIL import Image, ImageEnhance, ImageFilter
    original = source(root, job['input'])
    image = load_image(original)
    scale = number(job.get('scale', 1), 1, 4)
    size = (int(image.width * scale), int(image.height * scale))
    if size[0] * size[1] > 16_000_000:
        raise ValueError('Enhanced image exceeds the pixel budget')
    if job['operation'] == 'upscale':
        executable = installed_path(job['executable'])
        models = installed_path(job['models'], directory=True)
        model = job['model']
        if not re.fullmatch(r'[A-Za-z0-9_-]{1,80}', model):
            raise ValueError('Invalid local model name')
        for suffix in ('.bin', '.param'):
            installed_path(models / (model + suffix))
        integer(scale, 2, 4)
        process([executable, '-i', original, '-o', out / 'image.png', '-m', models,
                 '-n', model, '-s', str(scale)], timeout=600)
        image = load_image(out / 'image.png')
        if image.size != size:
            raise ValueError('Upscaler returned unexpected dimensions')
    else:
        image = image.resize(size, Image.Resampling.LANCZOS)
        for key, cls in [('contrast', ImageEnhance.Contrast), ('brightness', ImageEnhance.Brightness),
                         ('color', ImageEnhance.Color), ('sharpness', ImageEnhance.Sharpness)]:
            image = cls(image).enhance(number(job.get(key, 1), 0, 3))
        if job.get('denoise', False):
            image = image.filter(ImageFilter.MedianFilter(3))
    image.save(out / 'image.png', format='PNG')
    return {'dimensions': list(image.size), 'generative': False}


def web_assets(root, job, out):
    image = load_image(source(root, job['input']))
    icons = []
    for size in (16, 32, 72, 96, 128, 144, 152, 180, 192, 384, 512):
        name = f'icon-{size}x{size}.png'
        fitted(image, (size, size)).save(out / name, format='PNG')
        icons.append({'src': name, 'sizes': f'{size}x{size}', 'type': 'image/png'})
    fitted(image, (32, 32)).save(out / 'favicon.ico', format='ICO', sizes=[(16, 16), (32, 32)])
    fitted(image, (180, 180)).save(out / 'apple-touch-icon.png', format='PNG')
    if 'social_input' in job:
        social = load_image(source(root, job['social_input']))
        for name, dimensions in [('og-image.png', (1200, 630)), ('twitter-card.png', (1200, 600))]:
            fitted(social, dimensions).save(out / name, format='PNG')
    write_json(out / 'manifest.json', {'icons': icons})
    (out / 'meta.html').write_text('<link rel="icon" href="favicon.ico">\n'
                                  '<link rel="apple-touch-icon" href="apple-touch-icon.png">\n'
                                  '<link rel="manifest" href="manifest.json">\n', encoding='utf-8')
    return {'icons': len(icons), 'social_generated': 'social_input' in job}


def frames(root, job, maximum=90):
    names = job['frames']
    if not isinstance(names, list) or not 1 <= len(names) <= maximum:
        raise ValueError('Explicit frame list is empty or exceeds the budget')
    images = []
    pixels = 0
    for name in names:
        image = load_image(source(root, name))
        pixels += image.width * image.height
        if pixels > 32_000_000:
            raise ValueError('Frame sequence exceeds the decoded pixel budget')
        images.append(image)
    if len({im.size for im in images}) != 1:
        raise ValueError('Frame dimensions must agree')
    return images


def gif(root, job, out):
    from PIL import Image
    images = frames(root, job, 100)
    fps = integer(job.get('fps', 10), 1, 20)
    emoji = job.get('emoji', True)
    if len(images) < 2 or len(images) / fps > 5:
        raise ValueError('GIF needs 2+ frames and at most 5 seconds')
    size, cap = (128, 64 * 1024) if emoji else (480, 2 * 1024 * 1024)
    converted = []
    for frame in images:
        rgba = fitted(frame, (size, size))
        palette = rgba.convert('RGB').quantize(colors=47 if emoji else 127)
        palette.paste(255, mask=rgba.getchannel('A').point(lambda x: 255 if x < 128 else 0))
        converted.append(palette)
    path = out / 'animation.gif'
    converted[0].save(path, save_all=True, append_images=converted[1:], format='GIF',
                      duration=round(100 / fps) * 10, loop=0, transparency=255, disposal=2, optimize=False)
    with Image.open(path) as result:
        if result.n_frames < 2 or path.stat().st_size > cap:
            raise ValueError('GIF is static or oversized; simplify the frame sequence')
        return {'frames': result.n_frames, 'dimensions': list(result.size), 'bytes': path.stat().st_size}


def sticker_frames(images, emoji=False):
    from PIL import Image, ImageChops
    alpha = images[0].getchannel('A')
    for image in images[1:]:
        alpha = ImageChops.lighter(alpha, image.getchannel('A'))
    bounds = alpha.getbbox()
    if bounds is None or all(im.getchannel('A').getextrema() == (255, 255) for im in images):
        raise ValueError('Provide segmented RGBA images with visible content and transparency')
    size = 100 if emoji else 512
    margin = max(1, size // 20)
    result = []
    for image in images:
        canvas = Image.new('RGBA', (size, size))
        canvas.alpha_composite(fitted(image.crop(bounds), (size - 2 * margin, size - 2 * margin)), (margin, margin))
        result.append(canvas)
    return result


def sticker_static(root, job, out):
    image = sticker_frames([load_image(source(root, job['input']))], job.get('emoji', False))[0]
    path = out / 'sticker.webp'
    image.save(path, format='WEBP', lossless=True)
    if path.stat().st_size > 512 * 1024:
        raise ValueError('Static sticker exceeds 512 KiB; simplify the source')
    return {'dimensions': list(image.size), 'bytes': path.stat().st_size}


def sticker_video(root, job, out):
    images = sticker_frames(frames(root, job), job.get('emoji', False))
    fps = integer(job.get('fps', 30), 1, 30)
    if len(images) < 2 or len(images) / fps > 3:
        raise ValueError('Video must contain 2+ frames and last at most 3 seconds')
    ffmpeg, ffprobe = installed_path(job['ffmpeg']), installed_path(job['ffprobe'])
    size = images[0].width
    path = out / 'sticker.webm'
    raw = b''.join(im.tobytes() for im in images)
    process([ffmpeg, '-v', 'error', '-nostdin', '-f', 'rawvideo', '-pix_fmt', 'rgba',
             '-s', f'{size}x{size}', '-r', str(fps), '-i', 'pipe:0', '-an', '-c:v', 'libvpx-vp9',
             '-pix_fmt', 'yuva420p', '-auto-alt-ref', '0', '-b:v', '0', '-crf', '40', '-n', path], data=raw)
    info = json.loads(process([ffprobe, '-v', 'error', '-show_streams', '-show_format',
                               '-of', 'json', path], capture=True))
    streams = info['streams']
    if len(streams) != 1 or streams[0]['codec_name'] != 'vp9' or streams[0]['codec_type'] != 'video':
        raise ValueError('Encoded file is not a single VP9 video stream')
    stream = streams[0]
    if (stream['width'], stream['height']) != (size, size) or float(info['format']['duration']) > 3.05:
        raise ValueError('Encoded dimensions or duration are invalid')
    if path.stat().st_size > 256 * 1024:
        raise ValueError('Video exceeds 256 KiB; simplify the animation')
    decoded = process([ffmpeg, '-v', 'error', '-nostdin', '-c:v', 'libvpx-vp9', '-i', path,
                       '-f', 'rawvideo', '-pix_fmt', 'rgba', 'pipe:1'], capture=True)
    if len(decoded) != len(raw):
        raise ValueError('Decoded frame count differs from the source')
    expected, actual = raw[3::4], decoded[3::4]
    if not any(a < 128 for a in actual) or sum(abs(a-b) for a,b in zip(expected, actual)) / len(actual) > 12:
        raise ValueError('VP9 alpha did not survive decode; use a verified alpha-capable build')
    return {'frames': len(images), 'dimensions': [size, size], 'alpha_decode_verified': True}


def ocr_restore(root, job, out):
    text = runtime.read_limited(source(root, job['input'])).decode('utf-8')
    if len(text) > 1_000_000:
        raise ValueError('OCR text exceeds the character budget')
    cleaned = ''.join(c for c in text if unicodedata.category(c) != 'Cc' or c in '\n\r\t')
    cleaned = cleaned.replace('\ufeff', '').replace('\u00ad', '')
    changes = []
    for correction in job.get('corrections', []):
        old, new = correction['old'], correction['new']
        if not old or old not in cleaned or cleaned.count(old) != correction.get('count', 1):
            raise ValueError('OCR correction does not match the expected occurrence count')
        changes.append({'occurrences': cleaned.count(old)})
        cleaned = cleaned.replace(old, new)
    (out / 'restored.txt').write_bytes(cleaned.encode('utf-8'))
    report = {'changed': cleaned != text, 'corrections': changes, 'factual_accuracy_verified': False,
              'replacement_characters': cleaned.count('\ufffd')}
    write_json(out / 'review.json', report)
    return report


def ocr_extract(root, job, out):
    path = source(root, job['input'])
    load_image(path)
    executable = installed_path(job['executable'])
    language = job.get('language', 'eng')
    if not re.fullmatch(r'[a-zA-Z0-9_+]{1,80}', language):
        raise ValueError('Invalid OCR language selector')
    process([executable, path, out / 'ocr', '-l', language, '--psm',
             str(integer(job.get('psm', 3), 3, 13)), 'txt', 'tsv'])
    if not (out / 'ocr.txt').is_file() or not (out / 'ocr.tsv').is_file():
        raise ValueError('OCR engine did not produce both text and confidence coordinates')
    return {'text_and_coordinates': True, 'factual_accuracy_verified': False}


def union_mask(image, mask, threshold):
    from PIL import ImageChops, ImageFilter
    red, green, blue = image.convert('RGB').split()
    foreground = ImageChops.darker(ImageChops.darker(red, green), blue).point(
        lambda value: 255 if value < threshold else 0)
    combined = ImageChops.lighter(mask.convert('L'), foreground)
    combined = combined.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))
    return combined.point(lambda value: 0 if value < 60 else (255 if value > 180 else value))


def segment(root, job, out):
    from PIL import Image
    checkpoint = installed_path(job['rembg_checkpoint'])
    from rembg import new_session, remove
    images = frames(root, job) if 'frames' in job else [load_image(source(root, job['input']))]
    session = new_session('u2net_custom', model_path=str(checkpoint), providers=['CPUExecutionProvider'])
    cut = remove(images[0].convert('RGB'), session=session)
    seed = cut.getchannel('A')
    threshold = integer(job.get('white_threshold', 215), 1, 254)
    chroma = job.get('white_background', False)
    if chroma:
        seed = union_mask(images[0], seed, threshold)
    masks = {0: seed}
    if len(images) > 1:
        import numpy as np
        import torch
        from sam2.build_sam import build_sam2_video_predictor
        sam_checkpoint = installed_path(job['sam2_checkpoint'])
        config = job['sam2_config']
        if not re.fullmatch(r'configs/sam2(?:\.1)?/sam2(?:\.1)?_hiera_[a-z+]+\.yaml', config):
            raise ValueError('Use an installed SAM2 configuration, not arbitrary Hydra overrides')
        device = job.get('device', 'cpu')
        if device not in ('cpu', 'cuda'):
            raise ValueError('Select cpu or cuda explicitly')
        predictor = build_sam2_video_predictor(config, str(sam_checkpoint), device=device)
        with tempfile.TemporaryDirectory(prefix='.sam-frames-', dir=out) as directory:
            for index, image in enumerate(images):
                image.convert('RGB').save(Path(directory) / f'{index:05}.jpg', quality=95)
            with torch.inference_mode():
                state = predictor.init_state(video_path=directory, offload_video_to_cpu=True)
                predictor.add_new_mask(state, frame_idx=0, obj_id=1, mask=np.asarray(seed) > 127)
                for index, objects, logits in predictor.propagate_in_video(state):
                    if list(objects) != [1] or not 0 <= index < len(images):
                        raise ValueError('Unexpected SAM2 tracking result')
                    mask = (logits[0, 0] > 0).cpu().numpy().astype('uint8') * 255
                    masks[index] = Image.fromarray(mask)
        if set(masks) != set(range(len(images))):
            raise ValueError('SAM2 skipped requested frames')
    for index, image in enumerate(images):
        mask = union_mask(image, masks[index], threshold) if chroma else masks[index]
        image.putalpha(mask)
        image.save(out / f'frame-{index:04}.png', format='PNG')
    return {'frames': len(images), 'white_background_union': chroma, 'visual_review_required': True}


OPERATIONS = {'enhance': enhance, 'upscale': enhance, 'web-assets': web_assets, 'gif': gif,
              'sticker-static': sticker_static, 'sticker-video': sticker_video,
              'ocr-restore': ocr_restore, 'ocr-extract': ocr_extract, 'segment': segment}
