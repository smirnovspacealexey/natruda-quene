const channel = new BroadcastChannel('app-data');
let orderContainer = null;
let totalDisplay = null;
let total = 0;
let currOrder = [];


channel.addEventListener('message', (event) => {
    currOrder = JSON.parse(event.data);
    CalculateTotal();
    DisplayOrder();
});

$(document).ready(function () {
    orderContainer = $('#order-container');
    totalDisplay = $('#order-total-display');
})

function CalculateTotal() {
    total = 0;
    for (let i = 0; i < currOrder.length; i++) {
        total += currOrder[i]['price'] * currOrder[i]['quantity'];
    }
}

function DisplayOrder() {
    let tempHTML = "";

    function CreateOrderBlock(title, note, quantity, price) {
        return "<div class=\"order-item_container\">\n" +
            "                    <div class=\"order-item_text-info\">\n" +
            "                        <div class=\"order-item_title\">\n" +
            "                            <span>" + title + "</span>\n" +
            "                        </div>\n" +
            "                        <div class=\"order-item_note\">\n" +
            "                            <span>" + note + "</span>\n" +
            "                        </div>\n" +
            "                    </div>\n" +
            "                    <div class=\"order-item_quantity\">\n" +
            "                        x" + quantity + "\n" +
            "                    </div>\n" +
            "                    <div class=\"order-item_price\">\n" +
            "                        " + price + "p.\n" +
            "                    </div>\n" +
            "                </div>";
    }

    if (currOrder.length > 0) {
        for (let i = 0; i < currOrder.length; i++) {
            tempHTML += CreateOrderBlock(currOrder[i]['title'], currOrder[i]['note'], currOrder[i]['quantity'], currOrder[i]['price']);
        }
    } else {
        tempHTML += "<div class=\"order-item_container\">\n" +
            "                            <div class=\"order-item_text-info\">\n" +
            "                                <div class=\"order-item_title\">\n" +
            "                                    <span>Ждём Ваш Заказ!</span>\n" +
            "                                </div>\n" +
            "                            </div>\n" +
            "                        </div>";
    }

    tempHTML += "<div class=\"order-total\">\n" +
        "                    <div>Итого:</div>\n" +
        "                    <div class=\"order-total_display\" id=\"order-total-display\">" + total.toFixed(2) + "p.</div>\n" +
        "                </div>";

    orderContainer.html(tempHTML);
}