"""Graham Buddies — PyScript application logic (Event-Driven Programming).

Pattern used everywhere:
    USER EVENT  ->  Python event handler  ->  update data  ->  re-render the page

Handlers are connected with PyScript's @when(event, selector) decorator.
Buttons that are created dynamically (product cards, cart rows) are handled by
EVENT DELEGATION: one handler on the parent container checks which child was used.
"""
import asyncio
from pyscript import document, when, window

# ---------------------------------------------------------------- settings
DELIVERY_FEE = 50          # pesos, charged only for Delivery (edit me)
MAX_QTY = 99
VIDEO_URL = ""             # e.g. "promo.mp4" once you have a real ad

# ---------------------------------------------------------------- data (edit prices here)
PRODUCTS = [
    {"id": 1, "name": "Classic Mango Graham Cup", "category": "Cups", "price": 49, "size": "sm", "img": "MangoGrahamCup.jpg", "alt": "Three Mango Graham cups topped with cream, mango pieces and graham crumbs", "focus": "50% 50%",
     "desc": "A single-serving Mango Graham dessert.",
     "details": "Creamy layers, mango pieces and graham crumbs in one cup."},
    {"id": 2, "name": "Large Mango Graham Tub", "category": "Tubs", "price": 99, "size": "md", "img": "LargeMangoGraham.jpg", "alt": "Container of Mango Graham topped with sliced mango, with graham crackers and mangoes beside it", "focus": "50% 50%",
     "desc": "A larger serving for customers who want more.",
     "details": "A bigger tub of the same creamy mango and graham layers."},
    {"id": 3, "name": "Family-Size Mango Graham", "category": "Tubs", "price": 199, "size": "lg", "img": "FamilySizeMangoGraham.jpg", "alt": "Large tray of Mango Graham covered in graham crumbs and sliced mango", "focus": "50% 50%",
     "desc": "A larger dessert intended for sharing.",
     "details": "Made for family gatherings and sharing with friends."},
    {"id": 4, "name": "Mango Graham Overload", "category": "Specials", "price": 79, "size": "xl", "img": "MangoGrahamOver.jpg", "alt": "Two tubs of Mango Graham topped with diced mango", "focus": "50% 70%",
     "desc": "Extra mango and graham toppings.",
     "details": "A special variation with additional mango and graham toppings."},
]

cart = {}  # application state: {product_id: quantity}


# ---------------------------------------------------------------- helper (pure) functions
def peso(amount):
    """Format a number as Philippine pesos, e.g. 1234 -> ₱1,234."""
    return f"₱{amount:,}"


def find_product(product_id):
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product
    return None


def parse_quantity(text):
    """Return a valid whole-number quantity (1..MAX_QTY) or None if invalid."""
    try:
        quantity = int(str(text).strip())
    except ValueError:
        return None
    return quantity if 1 <= quantity <= MAX_QTY else None


def cart_count():
    return sum(cart.values())


def cart_subtotal():
    return sum(find_product(pid)["price"] * qty for pid, qty in cart.items())


def delivery_fee():
    mode = document.querySelector("#order-mode").value
    return DELIVERY_FEE if (mode == "Delivery" and cart) else 0


def validate_contact(name, contact):
    """Return a list of friendly error messages (empty list = valid)."""
    errors = []
    if len(name.strip()) < 2:
        errors.append("Please enter your name.")
    c = contact.strip()
    looks_like_email = "@" in c and "." in c.split("@")[-1] and " " not in c
    digits = [ch for ch in c if ch.isdigit()]
    looks_like_phone = len(digits) >= 7 and all(ch.isdigit() or ch in "+-() " for ch in c)
    if not (looks_like_email or looks_like_phone):
        errors.append("Enter a valid email or contact number.")
    return errors


# ---------------------------------------------------------------- UI helpers
def show_message(element_id, text, ok):
    box = document.querySelector(element_id)
    box.textContent = text
    box.className = "msg " + ("ok" if ok else "bad")
    box.hidden = False


async def _hide_toast():
    await asyncio.sleep(2.5)
    document.querySelector("#toast").classList.remove("show")


def toast(text):
    """Brief feedback message (e.g. 'Added to cart')."""
    box = document.querySelector("#toast")
    box.textContent = text
    box.classList.add("show")
    asyncio.ensure_future(_hide_toast())


# ---------------------------------------------------------------- rendering (dynamic page updates)
def render_products(category="all"):
    """Rebuild the product grid, showing only products in `category`."""
    html = ""
    for p in PRODUCTS:
        if category != "all" and p["category"] != category:
            continue
        html += f"""
        <article class="card">
          <div class="pimg"><img src="{p['img']}" alt="{p['alt']}" style="object-position:{p['focus']}" loading="lazy"></div>
          <div class="pb">
            <h3>{p['name']}</h3><p>{p['desc']}</p>
            <details><summary>Product details</summary><p>{p['details']}</p></details>
            <div class="price">{peso(p['price'])}</div>
            <div class="qrow">
              <label for="qty-{p['id']}">Qty</label>
              <input id="qty-{p['id']}" class="qty-in" type="number" min="1" max="{MAX_QTY}" value="1" data-qty="{p['id']}">
              <span class="live" id="live-{p['id']}">= {peso(p['price'])}</span>
            </div>
            <button class="btn btn-y" data-add="{p['id']}">Add to Cart</button>
          </div>
        </article>"""
    document.querySelector("#product-grid").innerHTML = html or "<p>No products match this filter.</p>"


def render_cart():
    """Rebuild the cart panel and every number that depends on the cart."""
    lines = ""
    for pid, qty in cart.items():
        p = find_product(pid)
        lines += f"""
        <div class="line"><strong>{p['name']}</strong><span>{peso(p['price'])} each</span>
          <div class="r">
            <div class="qty">
              <button data-dec="{pid}" aria-label="Decrease quantity">−</button>
              <input type="number" min="1" max="{MAX_QTY}" value="{qty}" data-set="{pid}" aria-label="Quantity for {p['name']}">
              <button data-inc="{pid}" aria-label="Increase quantity">+</button>
            </div>
            <strong>{peso(p['price'] * qty)}</strong>
            <button class="rm" data-remove="{pid}">Remove</button>
          </div></div>"""
    document.querySelector("#cart-lines").innerHTML = lines or '<p class="empty">Your cart is empty. Add a Mango Graham to get started!</p>'

    fee = delivery_fee()
    document.querySelector("#cart-count").textContent = str(cart_count())
    document.querySelector("#cart-subtotal").textContent = peso(cart_subtotal())
    document.querySelector("#cart-fee").textContent = peso(fee)
    document.querySelector("#cart-total").textContent = peso(cart_subtotal() + fee)

    has_items = len(cart) > 0
    checkout_open = not document.querySelector("#order-form").hidden
    document.querySelector("#go-checkout").hidden = (not has_items) or checkout_open
    if not has_items:
        document.querySelector("#order-form").hidden = True


def set_cart_open(is_open):
    panel = document.querySelector("#cart-panel")
    panel.classList.toggle("show", is_open)
    document.querySelector("#overlay").classList.toggle("show", is_open)
    panel.setAttribute("aria-hidden", "false" if is_open else "true")
    if is_open:
        document.querySelector("#close-cart").focus()


# ---------------------------------------------------------------- EVENT HANDLERS
# D. Product filtering — click on a filter chip
@when("click", "#filters")
def on_filter_click(event):
    chip = event.target.closest("[data-filter]")
    if chip is None:
        return
    for other in document.querySelectorAll("#filters .chip"):
        other.classList.remove("on")
    chip.classList.add("on")
    render_products(chip.getAttribute("data-filter"))


# B. User input — live price preview while typing a quantity on a product card
@when("input", "#product-grid")
def on_product_quantity_input(event):
    field = event.target
    pid_text = field.getAttribute("data-qty")
    if pid_text is None:
        return
    live = document.querySelector(f"#live-{pid_text}")
    quantity = parse_quantity(field.value)
    if quantity is None:
        live.textContent = f"Enter 1–{MAX_QTY}"
        live.className = "live err"
    else:
        live.textContent = "= " + peso(find_product(int(pid_text))["price"] * quantity)
        live.className = "live"


# A. Add to Cart — click on a product's button
@when("click", "#product-grid")
def on_add_to_cart(event):
    button = event.target.closest("[data-add]")
    if button is None:
        return
    pid = int(button.getAttribute("data-add"))
    quantity = parse_quantity(document.querySelector(f"#qty-{pid}").value)
    if quantity is None:
        toast(f"Please enter a quantity from 1 to {MAX_QTY}.")
        return
    cart[pid] = min(cart.get(pid, 0) + quantity, MAX_QTY)
    render_cart()
    toast(f"Added {quantity} × {find_product(pid)['name']} to your cart")


# B / E. Cart quantity buttons and Remove — one delegated click handler
@when("click", "#cart-lines")
def on_cart_click(event):
    target = event.target
    for attr, action in (("data-inc", "inc"), ("data-dec", "dec"), ("data-remove", "remove")):
        button = target.closest(f"[{attr}]")
        if button is None:
            continue
        pid = int(button.getAttribute(attr))
        if action == "inc":
            cart[pid] = min(cart[pid] + 1, MAX_QTY)
        elif action == "dec":
            cart[pid] -= 1
            if cart[pid] < 1:
                del cart[pid]
        else:
            del cart[pid]            # E. Cart removal
        render_cart()
        return


# B. Typing a quantity directly in the cart — validate, then recalculate
@when("change", "#cart-lines")
def on_cart_quantity_change(event):
    pid_text = event.target.getAttribute("data-set")
    if pid_text is None:
        return
    quantity = parse_quantity(event.target.value)
    if quantity is None:
        toast(f"Quantity must be a whole number from 1 to {MAX_QTY}.")
    else:
        cart[int(pid_text)] = quantity
    render_cart()                    # re-render restores a valid number


# Delivery vs Pickup — change event updates address field and fee
@when("change", "#order-mode")
def on_mode_change(event):
    pickup = event.target.value == "Pickup"
    document.querySelector("#o-address-wrap").hidden = pickup
    render_cart()


# C. Form submission — demo order
@when("submit", "#order-form")
def on_order_submit(event):
    event.preventDefault()           # stop the browser reloading the page
    name = document.querySelector("#o-name").value
    contact = document.querySelector("#o-contact").value
    mode = document.querySelector("#order-mode").value
    address = document.querySelector("#o-address").value
    errors = validate_contact(name, contact)
    if mode == "Delivery" and len(address.strip()) < 5:
        errors.append("Please enter a delivery address.")
    if not cart:
        errors.append("Your cart is empty.")
    if errors:
        show_message("#o-result", " ".join(errors), False)
        return
    total = peso(cart_subtotal() + delivery_fee())
    show_message("#o-result", f"Thanks, {name.strip()}! DEMO ONLY: your {mode.lower()} order ({total}) was not sent and no payment was taken.", True)
    cart.clear()
    document.querySelector("#order-form").reset()
    document.querySelector("#order-form").hidden = True
    render_cart()


# C. Form submission — contact inquiry
@when("submit", "#contact-form")
def on_contact_submit(event):
    event.preventDefault()
    name = document.querySelector("#c-name").value
    contact = document.querySelector("#c-contact").value
    message = document.querySelector("#c-message").value
    errors = validate_contact(name, contact)
    if len(message.strip()) < 5:
        errors.append("Please write a short message.")
    if errors:
        show_message("#c-result", " ".join(errors), False)
        return
    show_message("#c-result", f"Thank you, {name.strip()}! This is a local demonstration: your message was not sent to the business.", True)
    document.querySelector("#contact-form").reset()
    document.querySelector("#c-count").textContent = "0 / 300 characters"


# B. User input — live character counter
@when("input", "#c-message")
def on_message_input(event):
    text = event.target.value
    if len(text) > 300:
        event.target.value = text[:300]
        text = event.target.value
    document.querySelector("#c-count").textContent = f"{len(text)} / 300 characters"


# Cart open / close / checkout
@when("click", "#open-cart")
def on_open_cart(event):
    set_cart_open(True)


@when("click", "#close-cart")
def on_close_cart(event):
    set_cart_open(False)


@when("click", "#overlay")
def on_overlay_click(event):
    set_cart_open(False)


@when("keydown", "#cart-panel")
def on_cart_keydown(event):
    if event.key == "Escape":
        set_cart_open(False)


@when("click", "#go-checkout")
def on_go_checkout(event):
    document.querySelector("#order-form").hidden = False
    document.querySelector("#o-result").hidden = True
    render_cart()


# Navigation: mobile menu toggle and active link
@when("click", "#burger")
def on_burger_click(event):
    is_open = document.querySelector("#nav-links").classList.toggle("open")
    document.querySelector("#burger").setAttribute("aria-expanded", "true" if is_open else "false")


@when("click", "#nav-links")
def on_nav_click(event):
    link = event.target.closest("a")
    if link is None:
        return
    for other in document.querySelectorAll("#nav-links a"):
        other.classList.remove("on")
    link.classList.add("on")
    document.querySelector("#nav-links").classList.remove("open")
    document.querySelector("#burger").setAttribute("aria-expanded", "false")


# Promo video: preview a local file (placeholder until promo.mp4 is set)
def show_video(url):
    video = document.querySelector("#promo")
    video.src = url
    video.hidden = False
    document.querySelector("#video-placeholder").hidden = True


@when("change", "#video-file")
def on_video_file_chosen(event):
    chosen = event.target.files.item(0)
    if chosen is not None:
        show_video(window.URL.createObjectURL(chosen))


@when("keydown", "#video-pick")
def on_video_pick_key(event):
    if event.key in ("Enter", " "):
        event.preventDefault()
        document.querySelector("#video-file").click()


# ---------------------------------------------------------------- start-up
render_products("all")
render_cart()
if VIDEO_URL:
    show_video(VIDEO_URL)