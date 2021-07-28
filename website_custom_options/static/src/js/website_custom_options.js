odoo.define('website_custom_options.website_sale', function(require) {
    'use strict';

    require('web.dom_ready');
    var base = require('web_editor.base');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var utils = require('web.utils');
    var _t = core._t;
    var sAnimations = require('website.content.snippets.animation');
    require('website_sale.website_sale');

    if(!$('.oe_website_sale').length) {
        return $.Deferred().reject("DOM doesn't contain '.oe_website_sale'");
    }


    function price_to_str(price) {
        var l10n = _t.database.parameters;
        var precision = 2;

        if ($(".decimal_precision").length) {
            precision = parseInt($(".decimal_precision").last().data('precision'));
        }
        var formatted = _.str.sprintf('%.' + precision + 'f', price).split('.');
        formatted[0] = utils.insert_thousand_seps(formatted[0]);
        return formatted.join(l10n.decimal_point);
    }

    function calculatePrice($ul, $combinationPrice){
        var $parent = $ul.closest('.js_product');
        var $product_id = $parent.find('.product_id').first();
        var $price = $parent.find(".oe_price:first .oe_currency_value");
        var $website_price = $parent.find("[itemprop='price']");
        var $default_price = $parent.find(".oe_default_price:first .oe_currency_value");
        var $optional_price = $parent.find(".oe_optional:first .oe_currency_value");

        if($combinationPrice === undefined){
            $combinationPrice = parseFloat($website_price.text().replace('‑','-'));
        }

        var $option_data = $ul.data("option_data");
        if(_.isString($option_data)) {
            $option_data = JSON.parse($option_data.replace(/'/g, '"'));
            $ul.data('option_data', $option_data);
        }
        var $option_value_data = $ul.data("option_value_data");
        if(_.isString($option_value_data)) {
            $option_value_data = JSON.parse($option_value_data.replace(/'/g, '"'));
            $ul.data('option_value_data', $option_value_data);
        }
        var $option_public_data = $ul.data("option_public_data");
        if(_.isString($option_public_data)) {
            $option_public_data = JSON.parse($option_public_data.replace(/'/g, '"'));
            $ul.data('option_public_data', $option_public_data);
        }
        var $option_value_public_data = $ul.data("option_value_public_data");
        if(_.isString($option_value_public_data)) {
            $option_value_public_data = JSON.parse($option_value_public_data.replace(/'/g, '"'));
            $ul.data('option_value_public_data', $option_value_public_data);
        }


        if($.isEmptyObject($option_data)){
            return 0;
        }

        var $disableButton = false;
        var $additionalPrice = 0;
        var $additionalPublicPrice = 0;
        $parent.find("input.js_custom_option_change, textarea.js_custom_option_change").each(function () {
            var $input = $(this);
            var optionId = $input.attr('option_id');
            var isRequired = $input.attr('is_required');
            var inputData = $input.val();
            if(inputData){
                var $customOption = $input.closest(".custom_option");
                var $customOptionPrice = $option_data[optionId]
                if ($customOptionPrice){
                    $additionalPrice = $additionalPrice + parseFloat($customOptionPrice);
                }
                var $customOptionPrice = $option_public_data[optionId]
                if ($customOptionPrice){
                    $additionalPublicPrice = $additionalPublicPrice + parseFloat($customOptionPrice);
                }
            } else if(isRequired == "True"){
                $disableButton = true;
            };
        });
        $parent.find("select.js_custom_option_multiple_change").each(function () {
            var $input = $(this);
            var isRequired = $input.attr('is_required');
            var inputData = $input.val();
            var $customOptionPrice = 0.0;
            var $customOptionPublicPrice = 0.0;
            if(inputData){
                $.each($input.find(":selected"), function(){
                    var $selectedOption = $(this);
                    var $selectedOptionPrice = $option_value_data[$selectedOption.val()];
                    $customOptionPrice = $customOptionPrice + parseFloat($selectedOptionPrice);
                    var $selectedOptionPublicPrice = $option_value_public_data[$selectedOption.val()];
                    $customOptionPublicPrice = $customOptionPublicPrice + parseFloat($selectedOptionPublicPrice);
                });
                if ($customOptionPrice){
                    $additionalPrice = $additionalPrice + parseFloat($customOptionPrice);
                }
                if ($customOptionPublicPrice){
                    $additionalPublicPrice = $additionalPublicPrice + parseFloat($customOptionPublicPrice);
                }
            } else if(isRequired == "True"){
                $disableButton = true;
            };
        });

        $parent.find("input.js_custom_option_checkbox_change").each(function () {
            var radio_type = "radio";
            var checkbox_type = "checkbox";
            if(radio_type ==  $(this).attr("type")){
              var $input = $(this);
              var inputData = $input.val();
              var if_checked = $input.prop("checked")
              var isRequired = $input.attr('is_required');
              if (if_checked){
                if (inputData) {
                  var $selectedOption = $(this);
                  var $customOptionPrice = $option_value_data[$selectedOption.val()]
                  if ($customOptionPrice) {
                    $additionalPrice = $additionalPrice + parseFloat($customOptionPrice);
                  }
                  var $customOptionPublicPrice = $option_value_public_data[$selectedOption.val()]
                  if ($customOptionPrice){
                      $additionalPublicPrice = $additionalPublicPrice + parseFloat($customOptionPublicPrice);
                  }
                }
              }
              else if (isRequired == "True") {
                var count = 0;
                $input.closest('ul').find('li').each(function(){
                  var $options = $(this).find('.js_custom_option_checkbox_change');
                  if (! $options.prop("checked")){
                    if ($disableButton == false && count == 0){
                      $disableButton = true;
                    }
                  }
                  else{
                    $disableButton = false;
                    count = 1;
                  }
                })
              };
            }
            else if (checkbox_type ==  $(this).attr("type")){
              var $input = $(this);
              var inputData = $input.val();
              var if_checked = $input.prop("checked")
              var isRequired = $input.attr('is_required');
              if (if_checked){
                if (inputData) {
                  var $selectedOption = $(this);
                  var $customOptionPrice = $option_value_data[$selectedOption.val()]
                  if ($customOptionPrice) {
                    $additionalPrice = $additionalPrice + parseFloat($customOptionPrice);
                  }
                  var $customOptionPublicPrice = $option_value_public_data[$selectedOption.val()]
                  if ($customOptionPrice){
                      $additionalPublicPrice = $additionalPublicPrice + parseFloat($customOptionPublicPrice);
                  }
                }
              }
              else if (isRequired == "True") {
                var count = 0;
                $input.closest('ul').find('li').each(function(){
                  var $options = $(this).find('.js_custom_option_checkbox_change');
                  if (! $options.prop("checked")){
                    if ($disableButton == false && count == 0){
                      $disableButton = true;
                    }
                  }
                  else{
                    $disableButton = false;
                    count = 1;
                  }
                })
              };
            }
            if ($disableButton == true){
              return false;
            }
        });
        $price.html(price_to_str($combinationPrice+$additionalPrice));
        // $publicPrice.html(price_to_str(parseFloat($website_public_price.text().replace('‑','-'))+$additionalPublicPrice));
        if ($disableButton) {
            $parent.find("#add_to_cart").addClass("disabled");
        } else {
            $parent.find("#add_to_cart").removeClass("disabled");
        }
    }

    $('.oe_website_sale').each(function() {
        var oe_website_sale = this;

        $(oe_website_sale).on('change', 'input.js_custom_option_change, textarea.js_custom_option_change, select.js_custom_option_multiple_change, input.js_custom_option_checkbox_change', function (ev) {
            var $ul = $(ev.target).closest('.js_add_cart_custom_options');
            $("ul[data-attribute_exclusions]").change();
        });
    });

    sAnimations.registry.WebsiteSale.include({
        _onChangeCombination: function (ev, $parent, combination) {
            var def = this._super.apply(this, arguments);
            calculatePrice($('.js_add_cart_custom_options'), combination.price);
            return def;
        },
    });
});
