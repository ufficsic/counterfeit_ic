// $(document).ready(function () {
    $('#manufacturer').change(function () {
        $.ajax({
            url: '/ajax/selectedmanufacturer',
            type: 'POST',
            data: { manufacturer: this.value }
        })
            .done(function (data) {
                if (data.error) {
                    alert('Missing Data!')
                } else {
                    let products = data.products
                    let pOption = '<option value="' + -1 + '">' + 'Select a Product' + '</option>';
                    $.each(products, function (k, product) {
                        pOption += '<option value="' + product.id + '">' + product.name + '</option>';
                    })
                    $('#product').html(pOption);

                    let defect_types = data.defect_types
                    let dOption = '<option value="' + -1 + '">' + 'Select a Defect' + '</option>';
                    $.each(defect_types, function (k, defect_type) {
                        dOption += '<option value="' + defect_type.id + '">' + defect_type.name + '</option>';
                    })
                    $('#defect_type').html(dOption);
                }
            });
    });


    $('#product').change(function () {
        manufacturer = $('#manufacturer').val()
        product = this.value
        console.log(manufacturer, product)
        if (product === '-1') return
        $.ajax({
            url: '/ajax/selectedproduct',
            type: 'POST',
            data: { manufacturer: manufacturer, product: product }
        })
            .done(function (data) {
                if (data.error) {
                    alert('Missing Data!')
                } else {
                    console.log(data)
                    let defect_types = data.defect_types
                    let dOption = '<option value="' + -1 + '">' + 'Select a Defect' + '</option>';
                    $.each(defect_types, function (k, defect_type) {
                        dOption += '<option value="' + defect_type.id + '">' + defect_type.name + '</option>';
                    })
                    $('#defect_type').html(dOption);
                }
            });
    });


// });

// $(document).ready(function () {

// });
