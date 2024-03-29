/**
 * Created by paul on 03.11.17.
 */
/**
 * Created by paul on 10.07.17.
 */

$(document).ready(function () {
    $('#cook_interface').addClass('header-active');
    AdjustLineHeight();
    //GrillRefresher();
    Refresher();
    RightSideRefresher();
});
$(window).resize(AdjustLineHeight);


function GrillRefresher() {
    var url = $('#urls').attr('data-grill-timer-url');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    });
    $.ajax({
        type: 'POST',
        url: url,
        dataType: 'json',
        success: function (data) {
            $('div.in-grill-container').html(data['html']);
            var timer_text = $('div.in-grill-container .in-grill-timer');
            timer_text.text(function () {
                return this + " !";
            })
        },
        complete: function () {
            setTimeout(GrillRefresher, 10000);
        }
    });
}

function Refresher() {
    //console.log("NextRefresher");
    var url = $('#urls').attr('data-ajax');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    });
    $.ajax({
        type: 'POST',
        url: url,
        dataType: 'json',
        data: {'order_id': $('div.cook-daily-number').attr('order-id')},
        success: function (data) {
            //console.log("success");
            //console.log(data['html']);
            $('#selected-order-content').html(data['html']);
        },
        complete: function () {
            console.log('refresh')
            setTimeout(Refresher, 30000);
        }
    }).fail(function (jQXHR, textStatus, errorThrown) {
        alert("При попытке соединения с сервером произошла ошибка: " + jQXHR.status + " " + textStatus + " " + errorThrown);
    });
}

function RightSideRefresher() {
    //console.log("NextRefresher");
    var url = $('#urls').attr('data-ajax');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    });
    $.ajax({
        type: 'POST',
        url: url,
        dataType: 'json',
        data: {'order_id': $('div.cook-daily-number').attr('order-id')},
        success: function (data) {
            //console.log("success");
            //console.log(data['html']);
            $('#other-orders-queue').html(data['html_other']);
        },
        complete: function () {
            setTimeout(RightSideRefresher, 5000);
        }
    }).fail(function (jQXHR, textStatus, errorThrown) {
        alert("При попытке соединения с сервером произошла ошибка: " + jQXHR.status + " " + textStatus + " " + errorThrown);
    });
}


function AdjustLineHeight() {

}

function TakeItem(id) {
    var url = $('#urls').attr('data-take-url');
    var confirmation = true;
    console.log(confirmation);
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
                if (data['success']) {
                    $('#product_id_'+id.toString()).addClass('in-progress-item');
                    $('#product_id_'+id.toString()).attr('onclick', 'FinishItemCooking('+id+')');
                    //alert('Успех!');
                } else {
                    alert('Ужа делается ' + data['staff_maker'] + '!');
                }
            },
            complete: function () {
                location.reload();
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alert(textStatus + ' ' + errorThrown + ' ' + XMLHttpRequest);
            }
        }).fail(function (jQXHR, textStatus, errorThrown) {
            alert("При попытке соединения с сервером произошла ошибка: " + jQXHR.status + " " + textStatus + " " + errorThrown);
        });
    }

}

function ItemToGrill(id) {
    var url = $('#urls').attr('data-grill-url');
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
                //alert('Успех!' + data);
            },
            complete: function () {
                location.reload();
            }
        });
    }
}

function FinishItemCooking(id) {
    var url = $('#urls').attr('data-finish-url');
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
                    $('#product_id_'+id.toString()).addClass('in-grill-slot');
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


function SelectOrder(id) {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    });
    $.ajax({
            type: 'POST',
            url: $('#urls').attr('data-select-url'),
            data: {"order_id": id},
            dataType: 'json',
            success: function (data) {
                if(data['success']){
                    $('#selected-order-content').html(data['html']);
                }
            }
        }
    ).fail(function () {
        console.log('Failed ' + aux);
    });
}


function Pause() {
    $.ajax({
            type: 'POST',
            url: $('#urls').attr('pause-url'),
            success: function (data) {
                location.reload();
            }
        }
    ).fail(function () {
        console.log('Failed ' + aux);
    });
}
