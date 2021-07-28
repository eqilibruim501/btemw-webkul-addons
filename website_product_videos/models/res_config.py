#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################

from odoo import api, fields, models, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    wk_website_multi_video = fields.Boolean(string="Multi-Videos", help="""Enabling this setting will also enable multi image setting on your Odoo website.""")

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        IrDefault = self.env['ir.default'].sudo()
        IrDefault.set('res.config.settings','wk_website_multi_video', self.wk_website_multi_video)

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        IrDefault = self.env['ir.default'].sudo()
        res.update({
            'wk_website_multi_video':IrDefault.get('res.config.settings','wk_website_multi_video', self.wk_website_multi_video),
        })
        return res


class WebsiteProductVideoSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _name = 'website.product.video.settings'

    youtube_api_key = fields.Char(string="YouTube API Key",
                                  help="""YouTube API Key""",
                                  related="website_id.youtube_api_key", readonly=False)
    autoplay = fields.Boolean(string="Autoplay Video",
                                  help="""This parameter specifies whether the initial video will automatically start to play when the player loads.""",
                                  related="website_id.autoplay", readonly=False)
    controls = fields.Selection([('1', 'Show'), ('0', 'Hide')], string="Video Controls",
                                  help="""This parameter indicates whether the video player controls are displayed""",
                                  related="website_id.controls", readonly=False)
    rel = fields.Selection([('1', 'Show'), ('0', 'Hide')], string="Related Video",
                                  help="""This parameter indicates whether the player should show related videos when playback of the initial video ends.""",
                                  related="website_id.rel", readonly=False)
    fullscreen_video = fields.Boolean(string="Allow fullscreen Video",
                                  help="""Enable to fullscreen button from displaying in the player""",
                                  related="website_id.fullscreen_video", readonly=False)
    video_frameborder = fields.Integer(string="Video frameborder",
                                  help="""Add frameborder for youtube/vimeo videos""",
                                  related="website_id.video_frameborder", readonly=False)
    modestbranding = fields.Boolean(string="Modestbranding",
                                  help="""Modestbranding lets you use a YouTube player that does not show a YouTube logo.
                                  Note that a small YouTube text label will still display in the upper-right corner of a paused video when the user's mouse pointer hovers over the player."""
                                  ,related="website_id.modestbranding", readonly=False)
    loop = fields.Boolean(string="Loop Video",
                                  help="""Enable to set your video to repeat ad infinitum related videos.
                                  This parameter has limited support in the AS3 player and in IFrame embeds, which could load either the AS3 or HTML5 player.
                                  Currently, the loop parameter only works in the AS3 player when used in conjunction with the playlist parameter. """,
                                  related="website_id.loop", readonly=False)
    iv_load_policy = fields.Selection([('1', 'Show'), ('3', 'Hide')], string="Annotations Video",
                                  help="""Enable to show/hide annotations""",
                                  related="website_id.iv_load_policy", readonly=False)
    disablekb = fields.Boolean(string="Disable Keyboard Controls",
                                  help="""Enable to disable keyboard control on video.
                                  Currently supported keyboard controls are:
                                    * Spacebar or [k]: Play / Pause
                                    * Arrow Left: Jump back 5 seconds in the current video
                                    * Arrow Right: Jump ahead 5 seconds in the current video
                                    * Arrow Up: Volume up
                                    * Arrow Down: Volume Down
                                    * [f]: Toggle full-screen display
                                    * [j]: Jump back 10 seconds in the current video
                                    * [l]: Jump ahead 10 seconds in the current video
                                    * [m]: Mute or unmute the video
                                    * [0-9]: Jump to a point in the video.
                                            0 jumps to the beginning of the video, 1 jumps to the point 10% into the video, 2 jumps to the point 20% into the video, and so forth."""
                                    ,related="website_id.disablekb", readonly=False)
    video_height = fields.Integer(string="Video Height",
                                  help="""Video Height for youtube/vimeo videos"""
                                  ,related="website_id.video_height", readonly=False)
    video_width = fields.Integer(string="Video Width",
                                  help="""Video Width for youtube/vimeo videos"""
                                  ,related="website_id.video_width", readonly=False)
    popup_video = fields.Boolean(string="Allow Popup Video",
                                  help="""Enable to popup video on video click""",
                                  related="website_id.popup_video", readonly=False)
    autoplay_hover = fields.Boolean(string="Autoplay On Hover",
                                  help="""This parameter specifies whether the mouse hover video will automatically start to play when the player loads.""",
                                  related="website_id.autoplay_hover", readonly=False)
