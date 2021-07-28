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

from odoo import api, fields, models
import re
from odoo.exceptions import UserError
import requests
import json
import binascii
import logging
_logger = logging.getLogger(__name__)

class ProductVideo(models.Model):
    _name = "product.video"

    video_url = fields.Char(
        string='Url',
        required=True,
        help="Video Url of youtube or vimeo")
    video_id = fields.Char(
        string='Video Id',
        help="Video Id of youtube or vimeo")
    video_description = fields.Text(
        string='Description',
        help="Video description of youtube or vimeo")
    name = fields.Char('Title')
    use_description = fields.Boolean(string="Use as product description", default=True)
    exclude = fields.Boolean(string="Exclude from product multi videos", default=False)
    image = fields.Binary('Thumbnail', attachment=True)
    image_large = fields.Binary('Large Image', attachment=True)
    product_tmpl_id = fields.Many2one('product.template', 'Related Product', copy=True)
    website_ids = fields.Many2many('website')

    @api.onchange("image")
    def setImage(self):
        if self.image:
            self.image_large = self.image

    @api.onchange("video_url")
    def getDetails(self):
        videoUrl = self.video_url
        if videoUrl:
            if "vimeo" in videoUrl:
                videoUri = videoUrl.split("/")
                if len(videoUri) > 1:
                    videoId = videoUri[-1]
                    self.getVimeoData(videoId)
                else:
                    raise UserError("Video cant be shown due to the following reason: Invalid vimeo url")
            else:
                youtubeApiKey = self.env['website'].get_current_website().youtube_api_key
                if not youtubeApiKey:
                    raise UserError("Video cant be shown due to the following reason: Youtube API key is invalid")
                youtubeId = self.getVideoId()
                if youtubeId:
                    self.getYoutubeData(youtubeId, youtubeApiKey)

    def getVimeoData(self, videoId):
        apiUrl = "http://vimeo.com/api/v2/video/{}.json".format(videoId)
        videoObj = requests.get(apiUrl)
        if videoObj.status_code == 200:
            videoInfo = json.loads(videoObj.text)
            if videoInfo:
                items = videoInfo[0]
                if items:
                    title = items.get('title')
                    description = items.get('description')
                    imageLargeUrl = items.get('thumbnail_large')
                    imageUrl = items.get('thumbnail_medium')
                    proImageLarge = binascii.b2a_base64(requests.get(imageLargeUrl).content)
                    proImage = binascii.b2a_base64(requests.get(imageUrl).content)
                    self.name = title
                    self.video_id = videoId
                    self.video_description = description
                    self.image_large = proImageLarge
                    self.image = proImage
        return True

    def getYoutubeData(self, youtubeId, youtubeApiKey):
        youtubeUrl = "https://www.googleapis.com/youtube/v3/videos?part=snippet&id={}&key={}".format(youtubeId, youtubeApiKey)
        videoObj = requests.get(youtubeUrl)
        if videoObj.status_code == 200:
            videoInfo = json.loads(videoObj.text)
            if videoInfo.get('items'):
                items = videoInfo.get('items')[0]
                if items:
                    title = items.get('snippet').get('title')
                    description = items.get('snippet').get('description')
                    imageLargeUrl = items.get('snippet').get('thumbnails').get("high").get("url")
                    imageUrl = items.get('snippet').get('thumbnails').get("medium").get("url")
                    proImageLarge = binascii.b2a_base64(requests.get(imageLargeUrl).content)
                    proImage = binascii.b2a_base64(requests.get(imageUrl).content)
                    self.name = title
                    self.video_id = youtubeId
                    self.video_description = description
                    self.image_large = proImageLarge
                    self.image = proImage
        return True

    def getVideoId(self):
        youtubeId = False
        linkPattern = r'(?:https?:\/\/)?(?:[0-9A-Z-]+\.)?(?:youtube|youtu|youtube-nocookie)\.(?:com|be)\/(?:watch\?v=|watch\?.+&v=|embed\/|v\/|.+\?v=)?([^&=\n%\?]{11})'
        result = re.findall(linkPattern, self.video_url, re.MULTILINE | re.IGNORECASE)
        if result:
            youtubeId = result[0]
        return youtubeId

    def getEmbedUrl(self):
        videoUrl = self.video_url
        videoId = self.video_id
        if "vimeo" in videoUrl:
            if not videoId:
                videoUri = videoUrl.split("/")
                if len(videoUri) > 1:
                    videoId = videoUri[-1]
            url = "https://player.vimeo.com/video/{}?".format(videoId)
        else:
            if not videoId:
                videoId = self.getVideoId()
            url = "https://www.youtube.com/embed/{}?".format(videoId)
        url = self.getUpdatedUrl(url, videoId)
        return url

    def getUpdatedUrl(self, url, videoId):
        website_id = self.env['website'].get_current_website()

        autoplay = website_id.autoplay
        popup_video = website_id.popup_video
        if autoplay and popup_video:
            url += "&{}={}".format('autoplay', autoplay)

        controls = website_id.controls
        if controls:
            url += "&{}={}".format('controls', controls)

        rel = website_id.rel
        if rel:
            url += "&{}={}".format('rel', rel)
        
        modestbranding = website_id.modestbranding
        url += "&{}={}".format('modestbranding', modestbranding)

        loop = website_id.loop
        url += "&{}={}".format('loop', 1 if loop else 0)
        if loop:
            url += "&{}={}".format('playlist', videoId)

        iv_load_policy = website_id.iv_load_policy
        if iv_load_policy:
            url += "&{}={}".format('iv_load_policy', iv_load_policy)
        
        disablekb = website_id.disablekb
        url += "&{}={}".format('disablekb', disablekb)

        fs = website_id.fullscreen_video
        url += "&{}={}".format('fs', fs)
        
        return url


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_video_ids = fields.One2many('product.video', 'product_tmpl_id', string='Videos')

class Website(models.Model):
    _inherit = "website"

    youtube_api_key = fields.Char(string="YouTube API Key",
                                  help="""YouTube API Key""", default="AIzaSyD3TadJCd0Ww-QDpJfZqzMczPBiepFe-7E")
    autoplay = fields.Boolean(string="Autoplay Video",
                                  help="""This parameter specifies whether the initial video will automatically start to play when the player loads.""")
    controls = fields.Selection([('1', 'Show'), ('0', 'Hide')], string="Video Controls",
                                  help="""This parameter indicates whether the video player controls are displayed""", default=0)
    rel = fields.Selection([('1', 'Show'), ('0', 'Hide')], string="Related Video",
                                  help="""This parameter indicates whether the player should show related videos when playback of the initial video ends.""", default='1')
    fullscreen_video = fields.Boolean(string="Allow fullscreen Video",
                                  help="""Enable to fullscreen button from displaying in the player""")
    video_frameborder = fields.Integer(string="Video frameborder",
                                  help="""Add frameborder for youtube/vimeo videos""")
    modestbranding = fields.Boolean(string="Modestbranding",
                                  help="""Modestbranding lets you use a YouTube player that does not show a YouTube logo.
                                  Note that a small YouTube text label will still display in the upper-right corner of a paused video when the user's mouse pointer hovers over the player.""")
    loop = fields.Boolean(string="Loop Video",
                                  help="""Enable to set your video to repeat ad infinitum related videos.
                                  This parameter has limited support in the AS3 player and in IFrame embeds, which could load either the AS3 or HTML5 player.
                                  Currently, the loop parameter only works in the AS3 player when used in conjunction with the playlist parameter. """)
    iv_load_policy = fields.Selection([('1', 'Show'), ('3', 'Hide')], string="Annotations Video",
                                  help="""Enable to show/hide annotations""", default='3')
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
                                            0 jumps to the beginning of the video, 1 jumps to the point 10% into the video, 2 jumps to the point 20% into the video, and so forth.""",
                                    default=False)
    video_height = fields.Integer(string="Video Height",
                                  help="""Video Height for youtube/vimeo videos""", default="345")
    video_width = fields.Integer(string="Video Width",
                                  help="""Video Width for youtube/vimeo videos""", default="420")
    popup_video = fields.Boolean(string="Allow Popup Video",
                                  help="""Enable to popup video on video click""")
    autoplay_hover = fields.Boolean(string="Autoplay On Hover",
                                  help="""This parameter specifies whether the mouse hover video will automatically start to play when the player loads.""")
