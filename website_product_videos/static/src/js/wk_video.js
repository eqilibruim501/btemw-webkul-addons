/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
odoo.define('website_product_videos.wk_product_video', function (require) {
    "use strict";

    var rpc = require('web.rpc');
    var sAnimation = require('website.content.snippets.animation');

    sAnimation.registry.renderPopUpIframe = sAnimation.Class.extend({
        selector: "#wrap",
        read_events: {
            'click .wk_provideo': '_render_iframe'
        },
        _render_iframe: function(evt) {
            let $currentTarget = $(evt.currentTarget).find('.js_video_img');
            let pvid = $currentTarget.attr('data-pvid');
            console.log(pvid);
            
            $('#popupvideo').remove();
            rpc.query({
                route: '/shop/product/iframe',
                params: {
                    'pvid': pvid
                },
            }).then(function(data){
                $('#wrap').append(data);
                $('#popupvideo').modal('show');
            });
        }
    });

    $(document).ready(function() {

        var url = $(".wkmultivideo").attr('src');
        $('.wk_provideo').on('click', '.wk_image', function(e) {
            url = $(this).parent().find('.wk_video_url').val();
        });
        $(document).on('hidden.bs.modal','#popupvideo', function () {
            $(".wkmultivideo").attr('src', '');
          })
        $(document).on('show.bs.modal','#popupvideo', function () {
            $(".wkmultivideo").attr('src', url);
        });

        var wkhover = Boolean($('input.wk_hover').val());
        if (wkhover) {
            let videourl = '';
            $(".wk_descvideo" ).hover(function() {
                videourl = $(this).find('.wkmultivideo').attr('src');
                $(this).find('.wkmultivideo').attr('src', videourl + '&autoplay=1');
            }, function() {
                $(this).find('.wkmultivideo').attr('src', videourl);
            });
            $(document).on('mouseenter', ".carousel-item", function() {
                videourl = $(this).find('.wkmultivideo').attr('src');
                $(this).find('.wkmultivideo').attr('src', videourl + '&autoplay=1');
            })
            $(document).on('mouseleave', ".carousel-item", function() {
                $(this).find('.wkmultivideo').attr('src', videourl);
            });
            $(document).on('mouseenter', "#popupvideo .wkmultivideo", function() {
                videourl = $(this).attr('src');
                $(this).attr('src', videourl + '&autoplay=1');
            })
            $(document).on('mouseleave', "#popupvideo .wkmultivideo", function() {
                $(this).attr('src', videourl);
            });
        }
    });
})