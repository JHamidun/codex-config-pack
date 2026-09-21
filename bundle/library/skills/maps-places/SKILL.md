---
name: "maps-places"
description: "Поиск мест, адресов и геокодинг: 11 провайдеров — Google Places, Yandex Geosearch, 2GIS, OSM, Airbnb. Триггеры: «найди ресторан», «координаты адреса»."
---

# Codex execution contract

This recipe was adapted from a pinned public source. Its domain guidance is reusable;
its historical provider examples are not a live capability registry.

1. Resolve `${CODEX_PACK_ROOT}` from the installed `hamidun-pack` entrypoint. It is a documentation root, not an environment variable automatically created by Codex.
2. Native tool mapping: Claude `Read/Glob/Grep` means available file/search tools; `Bash` means the current shell; `Write/Edit/MultiEdit` means the supported patch/file tool. Claude `Task/Agent` means native collaboration with a concrete bounded subtask, only when delegation is authorized. Tool names inside old examples are illustrative, not callable API schemas.
3. Claude slash commands become catalog recipes. They are not automatically registered as Codex slash commands. Pass arguments explicitly in the task.
4. Do not execute files ending in `.source`, upstream hook examples, or paths containing `UPSTREAM_HOME`. They are quarantined reference code, NOT a validated runtime. A dependent workflow must first receive a reviewed Codex-owned adapter with explicit state/output roots and tests, or use an available native capability.
5. Do not load secrets, session databases, private memory, or Claude model/provider defaults. Resolve integrations and named environment variables only when required and authorized.
6. Model IDs, MCP names, permission snippets and scheduled-job examples in the source are historical. Check current supported equivalents. Never activate them just because a recipe mentions them.
7. Prefer native image generation, documents and browser tooling where available. Do not install dependencies or authorize a third party as a side effect of reading this recipe.
8. Preserve scope and output requirements. Mark unavailable dependencies clearly; do not claim a recipe passed a live test from a syntax/manifest check.

## Adapted domain recipe


# Maps & Places

Универсальный скилл для поиска организаций, мест, адресов через 11 провайдеров. Выбирает оптимальный по гео/задаче или мёрджит несколько.

## Когда использовать

- Поиск ресторанов, кафе, магазинов, заправок, аптек по запросу + локации
- Поиск конкурентов (organizations) в радиусе вокруг точки
- Геокодинг (адрес → координаты) и обратный (координаты → адрес)
- Получение часов работы, телефонов, рейтингов, рубрик, фото
- EV-зарядки на маршруте
- Airbnb-листинги с фильтром по датам и гостям
- Анализ плотности заведений / сетей в городе

## Провайдеры

| Провайдер | Лучше всего для | Лимиты бесплатно |
|-----------|------------------|------------------|
| **Google Places (New)** | Глобально, рейтинги, отзывы, цены ($), фото | $200/мес кредит ≈ 10K Text Search |
| **Yandex Geosearch** | РФ: часы, удобства, рубрики, телефоны | 1000/сутки |
| **2GIS Catalog** | РФ + СНГ: глубокая база, входы в здания, отделы | 1000/мес/сервис (demo) |
| **HERE Maps** | EU, Asia, Middle East, маршруты с трафиком | 250K транзакций/мес |
| **Mapbox** | Глобально, отличный dev-experience, навигация | 100K Search/Geocoding/мес |
| **Foursquare** | США/EU, 10K+ POI-категорий, Tips | $200 free credits/мес |
| **OpenCage** | Богатый геокодер: timezone, currency, sun rise | 2500/день |
| **OpenStreetMap Nominatim** | Free fallback геокодинг, bulk без квот | без ключа, 1 req/sec |
| **OpenStreetMap Overpass** | Bulk «все кафе в bbox», raw OSM queries | без ключа |
| **Open Charge Map** | EV-зарядки, community-managed | 100% free, no quota |
| **SerpAPI** | Fallback когда Places недоступен | 250/мес |
| **Apify Airbnb** | Airbnb-листинги с датами+гостями | pay-per-result ~$5/1K |

## Decision tree

```
Запрос пользователя
├── Геокодинг (адрес ↔ координаты)
│   ├── РФ → 2GIS + Yandex
│   ├── мир → Google + HERE + Mapbox
│   └── bulk без квот → Nominatim + OpenCage
├── Поиск организаций
│   ├── РФ → 2GIS (глубже) + Yandex (часы) + Google (рейтинги) [all]
│   ├── EU/Asia → HERE + Google + Foursquare [all+]
│   └── глобально → Google + Mapbox + Foursquare
├── EV-зарядки → ocm
├── Airbnb-листинги → airbnb (--check-in --check-out --guests)
└── Bulk POI экспорт → overpass
```

## Использование

### 1) CLI обёртка

```bash
# Отдельные провайдеры
python ${CODEX_PACK_ROOT}/library/tools/places_search.py google "ресторан грузинская" --lat 55.7558 --lon 37.6173
python ${CODEX_PACK_ROOT}/library/tools/places_search.py yandex "суши" --lat 55.7558 --lon 37.6173
python ${CODEX_PACK_ROOT}/library/tools/places_search.py 2gis "кофейня" --lat 55.7558 --lon 37.6173
python ${CODEX_PACK_ROOT}/library/tools/places_search.py here "georgian restaurant" --lat 55.7558 --lon 37.6173
python ${CODEX_PACK_ROOT}/library/tools/places_search.py mapbox "café" --lat 48.8566 --lon 2.3522
python ${CODEX_PACK_ROOT}/library/tools/places_search.py foursquare "pizza" --lat 40.7128 --lon -74.0060
python ${CODEX_PACK_ROOT}/library/tools/places_search.py opencage "Sample Beach, Brazil"
python ${CODEX_PACK_ROOT}/library/tools/places_search.py nominatim "Тверская 13"
python ${CODEX_PACK_ROOT}/library/tools/places_search.py overpass "cafe" --lat 55.7558 --lon 37.6173 --radius 1000 --limit 50
python ${CODEX_PACK_ROOT}/library/tools/places_search.py ocm "ev" --lat -22.971 --lon -43.182 --radius 50000
python ${CODEX_PACK_ROOT}/library/tools/places_search.py serpapi "pizza" --lat 40.71 --lon -74.00

# Airbnb
python ${CODEX_PACK_ROOT}/library/tools/places_search.py airbnb "Sample District, Brazil" --check-in 2026-07-01 --check-out 2026-07-08 --guests 2

# Гибридные merge-режимы
python ${CODEX_PACK_ROOT}/library/tools/places_search.py both "ресторан" --lat 55.7558 --lon 37.6173   # Yandex + Google
python ${CODEX_PACK_ROOT}/library/tools/places_search.py all  "кафе"     --lat 55.7558 --lon 37.6173   # +2GIS
python ${CODEX_PACK_ROOT}/library/tools/places_search.py all+ "ресторан" --lat 55.7558 --lon 37.6173   # +HERE + Foursquare + Mapbox (6 источников)

# JSON-выгрузка
python ${CODEX_PACK_ROOT}/library/tools/places_search.py all+ "пиццерия" --lat 55.75 --lon 37.62 --json > out.json

# Геокодинг (forward — все 6 провайдеров параллельно)
python ${CODEX_PACK_ROOT}/library/tools/places_search.py geocode "Мясницкая 13, Москва"

# Reverse геокодинг (все 6 параллельно)
python ${CODEX_PACK_ROOT}/library/tools/places_search.py reverse_geocode --lat 55.7558 --lon 37.6173
```

## Reference docs

- `references/google-places.md` — Places API (New): Text/Nearby Search, FieldMask, types
- `references/yandex-geosearch.md` — параметры spn/rspn, CompanyMetaData, Геокодер
- `references/2gis.md` — Catalog API, Places, Geocoder, Suggest
- `references/here-maps.md` — Discover/Browse, EV charging, PCS categories
- `references/mapbox.md` — Search Box, Geocoding v6, Directions, token types
- `references/foursquare.md` — v3 API, fsq_id, 10K+ категорий
- `references/opencage.md` — confidence levels, annotations (timezone, currency, sun)
- `references/nominatim.md` — User-Agent policy, polite 1 req/sec
- `references/overpass.md` — Overpass QL, amenity tags, bulk выборки
- `references/open-charge-map.md` — EV connection types, power tiers
- `references/serpapi-maps.md` — fallback scraping
- `references/yelp-fusion.md` — США/Canada/EU (требует business approval, ключа нет)
- `references/tripadvisor.md` — tourism (partner application only)
- `references/booking-affiliate.md` — hotels (partner only, альтернатива Apify)
- `references/china-maps.md` — Amap/Baidu (skip без кит. телефона)
- `references/geocoding.md` — forward/reverse normalization

## Грабли

1. **Yandex новые ключи активируются 30-45 минут**, не моментально — 403 «Invalid api key» после создания нормально, подожди
2. **2GIS demo key 1 месяц** и 1000/мес на каждый сервис. Перед production — оформить подписку
3. **Google `X-Goog-FieldMask` обязателен** — без него ошибка. Reviews/photos = другой ценовой SKU
4. **Yandex `ll` — `lon,lat`** (не lat,lon как у HERE/Google/Foursquare). **2GIS** тоже lon,lat. **Mapbox proximity** тоже lon,lat
5. **HERE billing требует $1 validation 3DS** на новые аккаунты — это auth-only, не списание; free 250K/мес
6. **Mapbox требует карту при signup** ($0 charge на free tier, но карта нужна для активации)
7. **Foursquare** — best signup via Google OAuth (избегает CAPTCHAs); требует прочитать Terms+Privacy перед Sign Up
8. **OCM требует User-Agent** в headers, иначе 403
9. **Nominatim User-Agent обязателен**, polite policy 1 req/sec — иначе блокирует. Контакт для него — `NOMINATIM_CONTACT` в `${CODEX_PACK_ROOT}/library/.credentials.master.env`; без него скрипт работает, но предупреждает в stderr (общий дефолтный адрес Nominatim банит целиком)
10. **Overpass timeout default 180s** — всегда `[timeout:25]`. `out center` для way/relation
11. **Merge tolerance 0.0005° (~50м)** — Google и Yandex могут давать одно место с >50м разницы
12. **Yandex Геокодер 403** — `YANDEX_GEOSEARCH_API_KEY` подключён только к Geosearch, для Geocoder API нужно «Привязать к API» в кабинете
13. **OpenCage оптимален для bulk address normalization** без POI-поиска

## Связано

- `${CODEX_PACK_ROOT}/library/templates/.credentials.master.env.example` — какие ключи включают каких провайдеров (раздел «Карты и геоданные»); Airbnb — `APIFY_API_TOKEN`
- `${CODEX_PACK_ROOT}/library/tools/places_search.py` — основной CLI (shim к скиллу)
- отдельный навык под Яндекс (в пак не входит) — Метрика/Директ/Диск (не карты)
- Skill `apify-scraping` — для Airbnb actor
- Skill `serpapi` — SERP scraping (включая google_maps)
