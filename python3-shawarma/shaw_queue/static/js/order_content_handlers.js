/**
 * Created by paul on 12.07.17.
 */
var status = $('#status-display');
var total_cost = 0;

function ReadyOrder(id) {
    var url = $('#urls').attr('data-ready-url');
    //var confirmation = confirm("Заказ готов?");
    //if (confirmation) {
    console.log(id + ' ' + url);
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    });
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'id': id,
            'servery_choose': $('[name=servery_choose]:checked').val()
        },
        dataType: 'json',
        success: function (data) {
            location.href = $('#current-queue').parent().attr('href');
            //if (data['success']) {
            //    alert('Success!');
            //}
        }
    });
    //}
}
function EditOrder(id) {
    var url = $('#urls').attr('edit-order-url');
    //var confirmation = confirm("Заказ готов?");
    //if (confirmation) {
    console.log(id + ' ' + url);
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    });
    $.ajax({
        type: 'GET',
        url: url,
        data: {
            'order_id': id,
            'modal_mode': true
        },
        dataType: 'json',
        success: function (data) {
            if (data['success']) {
                $('#modal-menu').html(data['html']);
                $('#modal-menu').css("display", "block");
                currOrder = data['order_content'];
                CalculateTotal();
                DrawOrderTable();
            }
        }
    });
    //}
}

function CaclculateTotalOC(quantity_inputs_values) {
    var prices = $('.quantityInput').map(
        function () {
            return parseFloat($(this).attr('cost'));
        }).get();
    var total_cost = 0;
    for (var i = 0; i < quantity_inputs_values.length; i++) {
        total_cost += prices[i] * quantity_inputs_values[i];
    }
    return total_cost;
}

function PayOrderCash(id) {
    var status = $('#status-display');
    var OK = $('#status-OK-button');
    var cancel = $('#status-cancel-button');
    var retry = $('#status-retry-button');
    var url = $('#urls').attr('data-pay-url');
    var loading_indiactor = $('#loading-indicator');
    var change_label = $('#order-change-label');
    var change = $('#order-change');
    var change_display = $('#change-display');
    var quantity_inputs_values = $('.quantityInput').map(
        function () {
            return parseFloat((this.value).replace(/,/g, '.'));
        }).get();
    var quantity_inputs_ids = $('.quantityInput').map(
        function () {
            return $(this).attr('item-id');
        }).get();
    total_cost = CaclculateTotalOC(quantity_inputs_values);
    var confirmation = false;
    if (total_cost > 5000)
        confirmation = confirm("Сумма заказа превышает 5000 р. Вы уверены в корректности ввода?");
    else
        confirmation = confirm("Оплатить заказ?");
    if (confirmation) {
        OK.prop('disabled', true);
        cancel.prop('disabled', true);
        retry.prop('disabled', true);
        loading_indiactor.show();
        status.text('Отправка заказа...');
        change.show();
        change.select();
        change_label.show();
        change_display.show();
        console.log(id + ' ' + url);
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        });
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'id': id,
                'values': JSON.stringify(quantity_inputs_values),
                'ids': JSON.stringify(quantity_inputs_ids),
                'paid_with_cash': JSON.stringify(true),
                'servery_id': $('[name=servery_choose]:checked').val()
            },
            dataType: 'json',
            success: function (data) {
                if (data['success']) {
                    alert("К оплате: " + data['total']);
                    ShowModalStatusOC();
                    status.text('Заказ №' + data.display_number + ' добавлен! Введите полученную сумму:');
                    setTimeout(function () {
                        StatusRefresherOC(data['guid']);
                    }, 1000);
                }
                else {
                    status.text(data['message']);
                    OK.prop('disabled', true);
                    cancel.prop('disabled', false);
                    retry.prop('disabled', false);
                    loading_indiactor.hide();
                }
                //if (data['success']) {
                //    alert('Success!');
                //}
            }
        });
    }
}

function CalculateCurrentCost() {
    // var message = ($.map($('input.quantityInput'), function (elem, i) {
    //     return parseFloat(elem.value)*parseFloat(elem.attr('cost')) || 0;
    // }).reduce(function (a, b) {
    //     return a + b;
    // }, 0));
    var message = 0;
    $('input.quantityInput').each(function () {
        console.log(message + " " + parseFloat($(this).val().replace(/,/g, '.')) + " " + parseFloat($(this).attr('cost')));
        message = message + parseFloat($(this).val().replace(/,/g, '.')) * parseFloat($(this).attr('cost'));
    });
    message = parseFloat(message).toFixed(2);
    alert(message + " р.");
}

function UpdateItemQuantity(event) {
    var url = $('#urls').attr('data-update-quantity-url');
    var quantity_inputs_values = parseFloat((event.target.value).replace(/,/g, '.'));
    var quantity_inputs_ids = $(event.target).attr('item-id');

    console.log(quantity_inputs_ids + " " + quantity_inputs_values + " " + $(event.target).is(':valid'));
    if ($(event.target).is(':valid')) {
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        });
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'new_quantity': JSON.stringify(quantity_inputs_values),
                'item_id': JSON.stringify(quantity_inputs_ids)
            },
            dataType: 'json',
            success: function (data) {
                if (!data['success']) {
                    alert(data['message']);
                }
                else {
                    $('#total-td').text(data['new_total']);
                }
            }
        });
    }
    else {
        alert('Количество введено неверно!');
    }

}

function PayOrderCard(id) {
    var status = $('#status-display');
    var OK = $('#status-OK-button');
    var cancel = $('#status-cancel-button');
    var retry = $('#status-retry-button');
    var retry_cash = $('#status-retry-cash-button');
    var loading_indiactor = $('#loading-indicator');
    var url = $('#urls').attr('data-pay-url');
    var quantity_inputs_values = $('.quantityInput').map(
        function () {
            return parseFloat((this.value).replace(/,/g, '.'));
        }).get();
    var quantity_inputs_ids = $('.quantityInput').map(
        function () {
            return $(this).attr('item-id');
        }).get();
    total_cost = CaclculateTotalOC(quantity_inputs_values);
    var confirmation = confirm("Заказ оплачен?");


    if (confirmation) {
        OK.prop('disabled', true);
        cancel.prop('disabled', true);
        retry.prop('disabled', true);
        loading_indiactor.show();
        status.text('Отправка заказа...');
        console.log(id + ' ' + url);
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        });
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'id': id,
                'values': JSON.stringify(quantity_inputs_values),
                'ids': JSON.stringify(quantity_inputs_ids),
                'paid_with_cash': JSON.stringify(false),
                'servery_id': $('[name=servery_choose]:checked').val()
            },
            dataType: 'json',
            success: function (data) {
                if (data['success']) {
                    ShowModalStatusOC();
                    status.text('Заказ №' + data.display_number + ' добавлен! Активация платёжного терминала...');
                    setTimeout(function () {
                        StatusRefresherOC(data['guid']);
                    }, 1000);
                }
                else {
                    status.text(data['message']);
                    OK.prop('disabled', true);
                    cancel.prop('disabled', false);
                    retry.prop('disabled', false);
                    loading_indiactor.hide();
                }
                           }
        });
    }
}

function PrintOrder(order_id) {
    $.get('/shaw_queue/order/print/' + order_id + '/');
}

function CancelItem(id) {
    var url = $('#urls').attr('data-cancel-item-url');
    var confirmation = confirm("Исключить из заказа?");
    if (confirmation) {
        console.log(id + ' ' + url);
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        });
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'id': id
            },
            dataType: 'json',
            success: function (data) {
                // if (data['success']) {
                //     alert('Успех!');
                // }
            },
            complete: function () {
                location.reload();
            }
        });
    }
}


function FinishCooking(id) {
    var url = $('#urls').attr('data-finish-item-url');
    console.log(id + ' ' + url);
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    });
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'id': id
        },
        dataType: 'json',
        success: function (data) {
            //alert('Success!' + data);
        },
        complete: function () {
            location.reload();
        }
    });
}


function GrillAllContent(id) {
    var url = $('#urls').attr('data-grill-all-content-url');
    var confirmation = true;
    if (confirmation) {
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        });
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'order_id': id
            },
            dataType: 'json',
            success: function (data) {
                //alert('Положите в заказ №' + data['order_number']);
            },
            complete: function () {
                location.reload();
            }
        });
    }
}


function FinishAllContent(id) {
    var url = $('#urls').attr('data-finish-all-content-url');
    var confirmation = true;
    if (confirmation) {
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        });
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'id': id
            },
            dataType: 'json',
            success: function (data) {
                //alert('Положите в заказ №' + data['order_number']);
            },
            complete: function () {
                location.reload();
            }
        });
    }
}

function ShowModalStatusOC() {
    var retry_cash = $('#status-retry-cash-button');
    var change_label = $('#order-change-label');
    var change = $('#order-change');

    // Get the modal
    var modal = document.getElementById('modal-status');
    //retry_cash.hide();

    modal.style.display = "block";
}

function CloseModalStatusOC() {
    var change_label = $('#order-change-label');
    var change = $('#order-change');
    var change_display = $('#change-display');
    var retry_cash = $('#status-retry-cash-button');
    var modal = document.getElementById('modal-status');

    change.val(0);
    change.hide();
    change_label.hide();
    change_display.text("Сдача...");
    change_display.hide();
    //retry_cash.hide();

    modal.style.display = "none";
}

function CalculateChangeOC() {
    var cash_input = $('#order-change');
    var change_display = $('#change-display');
    var change = parseFloat((cash_input.val()).replace(/,/g, '.')) - total_cost;
    change_display.text('Сдача ' + change + ' р.');
}

function OKHandelerOC() {
    CloseModalStatusOC();
    console.log('OKHandler fired.');
    location.reload();
}

function CancelHandlerOC() {
    CloseModalStatusOC();
    console.log('CancelHandler fired.');
    location.reload();
}

function RetryHandlerOC(id) {
    CloseModalStatusOC();
    PayOrderCard(id);
}

function RetryCashHandlerOC(id) {
    CloseModalStatus();
    PayOrderCash(id);
}


function StatusRefresherOC(guid) {
    var status = $('#status-display');
    var OK = $('#status-OK-button');
    var cancel = $('#status-cancel-button');
    var retry = $('#status-retry-button');
    var retry_cash = $('#status-retry-cash-button');
    var payment_choose = $('[name=payment_choose]:checked');
    var loading_indiactor = $('#loading-indicator');
    if (current_retries < max_retries) {
        current_retries++;
        status.text('Попытка ' + current_retries + ' из ' + max_retries);
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        });
        $.ajax({
                type: 'POST',
                url: $('#urls').attr('data-status-refresh-url'),
                data: {
                    "order_guid": guid
                },
                dataType: 'json',
                success: function (data) {
                    if (data['success']) {
                        switch (data['status']) {
                            case 0:
                                setTimeout(function () {
                                    StatusRefresherOC(data['guid']);
                                }, 1000);
                                break;
                            case 397:
                            case 396:
                            case 395:
                            case 394:
                            case 391:
                            case 390:
                                OK.prop('disabled', true);
                                cancel.prop('disabled', false);
                                retry.prop('disabled', false);
                                if (payment_choose.val() != "paid_with_cash")
                                    retry_cash.show();
                                break;
                            // case 396:
                            //     OK.prop('disabled', true);
                            //     cancel.prop('disabled', false);
                            //     retry.prop('disabled', false);
                            //     break;
                            case 393:
                            case 392:
                                if (payment_choose == "paid_with_cash")
                                    status.text('Заказ №' + data.daily_number + '. ' + data['message'] + ' Введите полученную сумму, отдайте клиенту сдачу и нажмите ОК');
                                else
                                    status.text('Заказ №' + data.daily_number + '. ' + data['message'] + ' проведён в 1С! Операция безналичного расчёта завершена успешно! Нажмите ОК');
                                OK.prop('disabled', false);
                                cancel.prop('disabled', true);
                                retry.prop('disabled', true);
                                OK.focus();
                                break;
                            case 200:
                                if (payment_choose.val() == "paid_with_cash")
                                    status.text('Заказ №' + data.daily_number + ' проведён в 1С! Введите полученную сумму, отдайте клиенту сдачу и нажмите ОК');
                                else
                                    status.text('Заказ №' + data.daily_number + ' проведён в 1С! Операция безналичного расчёта завершена успешно! Нажмите ОК');
                                OK.prop('disabled', false);
                                cancel.prop('disabled', true);
                                retry.prop('disabled', true);
                                OK.focus();
                                break;
                            default:
                                OK.prop('disabled', true);
                                cancel.prop('disabled', false);
                                retry.prop('disabled', false);
                                break;
                        }
                        if (data['status'] != 0)
                            loading_indiactor.hide();
                        if (data['status'] != 200)
                            status.text('Заказ №' + data.daily_number + '. ' + data['message']);
                    }
                    else {
                        OK.prop('disabled', true);
                        cancel.prop('disabled', false);
                        retry.prop('disabled', false);
                        status.text(data['message']);
                        loading_indiactor.hide();
                    }
                }
            }
        ).fail(function () {
            OK.prop('disabled', false);
            cancel.prop('disabled', true);
            retry.prop('disabled', true);
            loading_indiactor.hide();
            status.text('Необработанное исключение!');
        });
    }
    else {
        OK.prop('disabled', false);
        cancel.prop('disabled', true);
        retry.prop('disabled', true);
        status.text('Превышено количество попыток!');
    }
}
