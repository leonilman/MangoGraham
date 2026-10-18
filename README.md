# Graham Buddies — Mango Graham Website (HTML + CSS + PyScript)

Event-Driven Programming final project. HTML = structure, CSS = design, **PyScript (Python) = all interactivity**.

## Run it
PyScript loads `main.py` with `fetch`, so open the folder through a local server (double-clicking `index.html` will not work):

```bash
cd graham-buddies
python -m http.server 8000
# open http://localhost:8000
```
An internet connection is needed for the PyScript CDN (release 2024.11.1) and Google Fonts. The first load takes a few seconds while Python starts in the browser.

## Files
| File | Purpose |
|---|---|
| `index.html` | Page structure and PyScript setup |
| `styles.css` | Palette, layout, responsive design, reduced-motion |
| `main.py` | Python data, helper functions and event handlers |
| `logo.jpg` | Official logo, used unchanged |
| `Header.jpg` | Hero photo |
| `MangoGraham*.jpg`, `LargeMangoGraham.jpg`, `FamilySizeMangoGraham.jpg` | Product photos |

## Event-driven map (all in `main.py`)
| Event | Handler | Result |
|---|---|---|
| click filter chip | `on_filter_click` | catalog re-filtered |
| input on quantity | `on_product_quantity_input` | live price preview / error |
| click Add to Cart | `on_add_to_cart` | cart count + totals update, toast |
| click +, −, Remove | `on_cart_click` | quantities/removal, totals update |
| change cart quantity | `on_cart_quantity_change` | validated and recalculated |
| change Delivery/Pickup | `on_mode_change` | address field + delivery fee |
| submit order / contact form | `on_order_submit`, `on_contact_submit` | validation errors or demo confirmation |
| input message | `on_message_input` | live character counter |

## Customize
- Prices, names, descriptions: `PRODUCTS` list in `main.py`. Delivery fee: `DELIVERY_FEE`.
- Real ad: add `promo.mp4`, set `VIDEO_URL = "promo.mp4"`.
- Product photos: put images in `` and set each product's `"img"` in `PRODUCTS` (`main.py`).
- Business contact details, social links and reviews are placeholders in `index.html`.

## Demo notes
Checkout and contact forms are local demos: nothing is sent and no payment is processed. Testimonials are sample content.

## Team contributions
_Each member should add their own meaningful commits and list their contributions here._
