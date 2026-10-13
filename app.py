
from flask import Flask, render_template, request, redirect, url_for, flash
from blockchain import supply_chain

app = Flask(__name__)
app.secret_key = "blocktrace-demo-secret-key"


@app.template_filter("datetimeformat")
def datetimeformat(value):
    return time.strftime(
        "%d %b %Y, %I:%M:%S %p",
        time.localtime(value)
    )



@app.route("/")
def index():
    return render_template(
        "index.html",
        products=supply_chain.products,
        chain=supply_chain.chain,
        chain_valid=supply_chain.verify_chain()
    )


@app.route("/register", methods=["POST"])
def register():
    product_id = request.form.get("product_id", "").strip()
    name = request.form.get("name", "").strip()
    category = request.form.get("category", "").strip()
    manufacturer = request.form.get("manufacturer", "").strip()
    origin = request.form.get("origin", "").strip()

    if not all([product_id, name, category, manufacturer, origin]):
        flash("Please fill in all product details.", "error")
        return redirect(url_for("index"))

    success, message = supply_chain.register_product(
        product_id, name, category, manufacturer, origin
    )

    flash(message, "success" if success else "error")
    return redirect(url_for("index"))


@app.route("/update", methods=["POST"])
def update():
    product_id = request.form.get("product_id", "").strip()
    status = request.form.get("status", "").strip()
    location = request.form.get("location", "").strip()

    allowed_statuses = [
        "Manufactured",
        "Packed",
        "In Transit",
        "At Warehouse",
        "Out for Delivery",
        "Delivered"
    ]

    if not product_id or not location or status not in allowed_statuses:
        flash("Please enter valid shipment details.", "error")
        return redirect(url_for("index"))

    success, message = supply_chain.add_update(
        product_id, status, location
    )

    flash(message, "success" if success else "error")
    return redirect(url_for("index"))


@app.route("/track", methods=["GET", "POST"])
def track():
    product = None
    history = []
    searched_id = ""

    if request.method == "POST":
        searched_id = request.form.get("product_id", "").strip()
        product = supply_chain.products.get(searched_id)
        history = supply_chain.get_product_history(searched_id)

        if not product:
            flash("No product found with that ID.", "error")

    return render_template(
        "index.html",
        products=supply_chain.products,
        chain=supply_chain.chain,
        chain_valid=supply_chain.verify_chain(),
        tracked_product=product,
        history=history,
        searched_id=searched_id
    )


@app.route("/verify")
def verify():
    return {
        "chain_valid": supply_chain.verify_chain(),
        "total_blocks": len(supply_chain.chain),
        "message": (
            "Blockchain integrity check passed."
            if supply_chain.verify_chain()
            else "Warning: blockchain integrity check failed."
        )
    }


if __name__ == "__main__":
    app.run(debug=True)
