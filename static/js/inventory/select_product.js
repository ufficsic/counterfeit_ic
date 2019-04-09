$(document).ready(function () {
    $('#manufacturer').change(function () {
        $.ajax({
            url: '/ajax/getproducts',
            type: 'POST',
            data: { manufacturer: this.value }
        })
            .done(function (data) {
                if (data.error) {
                    alert('Missing Data!')
                } else {
                    let products = data.products
                    let option = '<option value="' + -1 + '">' + 'Select a Product' + '</option>';
                    $.each(products, function (k, product) {
                        option += '<option value="' + product.id + '">' + product.name + '</option>';
                    })
                    $('#product').html(option);
                }
            });
    });
});
