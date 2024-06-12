# -*- coding: utf-8 -*-
import logging
from typing import Any, Callable, Dict, Optional

from .clients import ws_base
from .models import web as web_models, open_live as open_models

__all__ = (
    "HandlerInterface",
    "BaseHandler",
)

logger = logging.getLogger("blivedm")

logged_unknown_cmds = {
    "COMBO_SEND",
    "ENTRY_EFFECT",
    "HOT_RANK_CHANGED",
    "HOT_RANK_CHANGED_V2",
    # 'INTERACT_WORD', # 进入直播间
    # 'LIVE',
    "LIVE_INTERACTIVE_GAME",
    "NOTICE_MSG",
    "ONLINE_RANK_COUNT",
    "ONLINE_RANK_TOP3",
    "ONLINE_RANK_V2",
    "PK_BATTLE_END",
    "PK_BATTLE_ENTRANCE",
    "PK_BATTLE_FINAL_PROCESS",
    "PK_BATTLE_MATCH_TIMEOUT",
    "PK_BATTLE_PRE",
    "PK_BATTLE_PRE_NEW",
    "PK_BATTLE_PROCESS",
    "PK_BATTLE_PROCESS_NEW",
    "PK_BATTLE_SETTLE",
    "PK_BATTLE_SETTLE_NEW",
    "PK_BATTLE_SETTLE_USER",
    "PK_BATTLE_SETTLE_V2",
    "PK_BATTLE_START",
    "PK_BATTLE_START_NEW",
    "PK_BATTLE_VIDEO_PUNISH_BEGIN",
    "PK_BATTLE_VIDEO_PUNISH_END",
    # 'PREPARING',
    "ROOM_REAL_TIME_MESSAGE_UPDATE",
    "STOP_LIVE_ROOM_LIST",
    "SUPER_CHAT_MESSAGE_JPN",
    "WIDGET_BANNER",
    "WATCHED_CHANGE",
    "LIVE_MULTI_VIEW_CHANGE",
    "COMMON_NOTICE_DANMAKU",  # BLS秋季限时任务：任务即将结束，抓紧完成获取10元红包奖励吧！未完成任务进度将无法获得奖励 https://st.openbayes.net/organizations/openbayes/issues/732/events/1fcc24e45ef34148b3193fb676dffc5a/?project=13&query=is%3Aunresolved
    "DANMU_AGGREGATION",  # 老板大气！点点红包抽礼物, https://st.openbayes.net/organizations/openbayes/issues/732/events/aafcb5e6c02b45af8de99a26175e25fe/?project=13&query=is%3Aunresolved
    "HOT_RANK_SETTLEMENT",  # 恭喜主播 <% 阿梓从小就很可爱 %> 荣登限时热门榜虚拟主播榜top10! 即将获得热门流量推荐哦！
    "HOT_RANK_SETTLEMENT_V2",  # 恭喜主播 <% 老实憨厚的笑笑 %> 荣登限时热门榜户外榜榜首! 即将获得热门流量推荐哦！
}
"""已打日志的未知cmd"""


class HandlerInterface:
    """
    直播消息处理器接口
    """

    def handle(self, client: ws_base.WebSocketClientBase, command: dict):
        raise NotImplementedError

    def on_client_stopped(
        self, client: ws_base.WebSocketClientBase, exception: Optional[Exception]
    ):
        """
        当客户端停止时调用。可以在这里close或者重新start
        """


def _make_msg_callback(method_name, message_cls):
    def callback(
        self: "BaseHandler", client: ws_base.WebSocketClientBase, command: dict
    ):
        method = getattr(self, method_name)
        return method(client, message_cls.from_command(command["data"]))

    return callback


def _make_raw_msg_callback(method_name, message_cls, raw=False):
    def callback(
        self: "BaseHandler", client: ws_base.WebSocketClientBase, command: dict
    ):
        method = getattr(self, method_name)
        return method(
            client, message_cls.from_command(command if raw else command["data"])
        )

    return callback


class BaseHandler(HandlerInterface):
    """
    一个简单的消息处理器实现，带消息分发和消息类型转换。继承并重写_on_xxx方法即可实现自己的处理器
    """

    def __danmu_msg_callback(self, client: ws_base.WebSocketClientBase, command: dict):
        return self._on_danmaku(
            client, web_models.DanmakuMessage.from_command(command["info"])
        )

    _CMD_CALLBACK_DICT: Dict[
        str, Optional[Callable[["BaseHandler", ws_base.WebSocketClientBase, dict], Any]]
    ] = {
        # 收到心跳包，这是blivedm自造的消息，原本的心跳包格式不一样
        "_HEARTBEAT": _make_msg_callback("_on_heartbeat", web_models.HeartbeatMessage),
        # 收到弹幕
        # go-common\app\service\live\live-dm\service\v1\send.go
        "DANMU_MSG": __danmu_msg_callback,
        # 有人送礼
        "SEND_GIFT": _make_msg_callback("_on_gift", web_models.GiftMessage),
        # 有人上舰
        "GUARD_BUY": _make_msg_callback("_on_buy_guard", web_models.GuardBuyMessage),
        # 醒目留言
        "SUPER_CHAT_MESSAGE": _make_msg_callback(
            "_on_super_chat", web_models.SuperChatMessage
        ),
        # 删除醒目留言
        "SUPER_CHAT_MESSAGE_DELETE": _make_msg_callback(
            "_on_super_chat_delete", web_models.SuperChatDeleteMessage
        ),
        # eop-blive 自定义事件
        "LIVE": _make_raw_msg_callback("_on_live", web_models.LiveMessage, True),
        "PREPARING": _make_raw_msg_callback(
            "_on_preparing", web_models.PreparingMessage, True
        ),
        "INTERACT_WORD": _make_raw_msg_callback(
            "_on_interact_word", web_models.InteractWordMessage
        ),
        "USER_TOAST_MSG": _make_raw_msg_callback(
            "_on_user_toast", web_models.UserToastMessage
        ),
        "USER_VIRTUAL_MVP": _make_raw_msg_callback(
            "_on_virtual_mvp", web_models.UserVirtualMvp
        ),
        "WARNING": _make_raw_msg_callback(
            "_on_warning", web_models.WarningMessage, True
        ),
        "CUT_OFF": _make_raw_msg_callback(
            "_on_cut_off", web_models.CutOffMessage, True
        ),
        "ROOM_SILENT_ON": _make_raw_msg_callback(
            "_on_room_silent_on", web_models.RoomSilentOnMessage
        ),
        "ROOM_SILENT_OFF": _make_raw_msg_callback(
            "_on_room_silent_off", web_models.RoomSilentOffMessage
        ),
        "ROOM_ADMINS": _make_raw_msg_callback(
            "_on_room_admins", web_models.RoomAdminsMessage, True
        ),
        # yes this is the lowercased event from ws 😅
        "room_admin_entrance": _make_raw_msg_callback(
            "_on_room_admin_entrance", web_models.RoomAdminEntranceMessage, True
        ),
        "ROOM_ADMIN_REVOKE": _make_raw_msg_callback(
            "_on_room_admin_revoke", web_models.RoomAdminRevokeMessage, True
        ),
        "ROOM_BLOCK_MSG": _make_raw_msg_callback(
            "_on_room_block", web_models.RoomBlockMessage
        ),
        #
        # 开放平台消息
        #
        # 收到弹幕
        "LIVE_OPEN_PLATFORM_DM": _make_msg_callback(
            "_on_open_live_danmaku", open_models.DanmakuMessage
        ),
        # 有人送礼
        "LIVE_OPEN_PLATFORM_SEND_GIFT": _make_msg_callback(
            "_on_open_live_gift", open_models.GiftMessage
        ),
        # 有人上舰
        "LIVE_OPEN_PLATFORM_GUARD": _make_msg_callback(
            "_on_open_live_buy_guard", open_models.GuardBuyMessage
        ),
        # 醒目留言
        "LIVE_OPEN_PLATFORM_SUPER_CHAT": _make_msg_callback(
            "_on_open_live_super_chat", open_models.SuperChatMessage
        ),
        # 删除醒目留言
        "LIVE_OPEN_PLATFORM_SUPER_CHAT_DEL": _make_msg_callback(
            "_on_open_live_super_chat_delete", open_models.SuperChatDeleteMessage
        ),
        # 点赞
        "LIVE_OPEN_PLATFORM_LIKE": _make_msg_callback(
            "_on_open_live_like", open_models.LikeMessage
        ),
    }  # type: ignore
    """cmd -> 处理回调"""

    def handle(self, client: ws_base.WebSocketClientBase, command: dict):
        cmd = command.get("cmd", "")
        pos = cmd.find(":")  # 2019-5-29 B站弹幕升级新增了参数
        if pos != -1:
            cmd = cmd[:pos]

        if cmd not in self._CMD_CALLBACK_DICT:
            # 只有第一次遇到未知cmd时打日志
            if cmd not in logged_unknown_cmds:
                logger.warning(
                    "room=%d unknown cmd=%s, command=%s", client.room_id, cmd, command
                )
                logged_unknown_cmds.add(cmd)
            return

        callback = self._CMD_CALLBACK_DICT[cmd]
        if callback is not None:
            callback(self, client, command)

    def _on_heartbeat(
        self, client: ws_base.WebSocketClientBase, message: web_models.HeartbeatMessage
    ):
        """
        收到心跳包
        """

    def _on_danmaku(
        self, client: ws_base.WebSocketClientBase, message: web_models.DanmakuMessage
    ):
        """
        收到弹幕
        """

    def _on_gift(
        self, client: ws_base.WebSocketClientBase, message: web_models.GiftMessage
    ):
        """
        收到礼物
        """

    def _on_buy_guard(
        self, client: ws_base.WebSocketClientBase, message: web_models.GuardBuyMessage
    ):
        """
        有人上舰
        """

    def _on_super_chat(
        self, client: ws_base.WebSocketClientBase, message: web_models.SuperChatMessage
    ):
        """
        醒目留言
        """

    def _on_super_chat_delete(
        self,
        client: ws_base.WebSocketClientBase,
        message: web_models.SuperChatDeleteMessage,
    ):
        """
        删除醒目留言
        """

    # eop-blive 自定义事件
    def _on_live(
        self,
        client: ws_base.WebSocketClientBase,
        message: web_models.LiveMessage,
    ):
        """
        _on_live
        """

    def _on_preparing(
        self,
        client: ws_base.WebSocketClientBase,
        message: web_models.PreparingMessage,
    ):
        """
        _on_preparing
        """

    def _on_interact_word(
        self,
        client: ws_base.WebSocketClientBase,
        message: web_models.InteractWordMessage,
    ):
        """
        _on_interact_word
        """

    def _on_user_toast(
        self, client: ws_base.WebSocketClientBase, message: web_models.UserToastMessage
    ):
        """
        _on_user_toast
        """

    def _on_virtual_mvp(
        self, client: ws_base.WebSocketClientBase, message: web_models.UserVirtualMvp
    ):
        """
        _on_virtual_mvp
        """

    def _on_warning(
        self, client: ws_base.WebSocketClientBase, message: web_models.WarningMessage
    ):
        """
        _on_warning
        """

    def _on_cut_off(
        self, client: ws_base.WebSocketClientBase, message: web_models.CutOffMessage
    ):
        """
        _on_cut_off
        """

    def _on_room_silent_on(
        self,
        client: ws_base.WebSocketClientBase,
        message: web_models.RoomSilentOnMessage,
    ):
        """
        _on_room_silent_on
        """

    def _on_room_silent_off(
        self,
        client: ws_base.WebSocketClientBase,
        message: web_models.RoomSilentOffMessage,
    ):
        """
        _on_room_silent_off
        """

    def _on_room_admins(
        self, client: ws_base.WebSocketClientBase, message: web_models.RoomAdminsMessage
    ):
        """
        _on_room_admins
        """

    def _on_room_admin_entrance(
        self,
        client: ws_base.WebSocketClientBase,
        message: web_models.RoomAdminEntranceMessage,
    ):
        """
        _on_room_admin_entrance
        """

    def _on_room_admin_revoke(
        self,
        client: ws_base.WebSocketClientBase,
        message: web_models.RoomAdminRevokeMessage,
    ):
        """
        _on_room_admin_revoke
        """

    def _on_room_block(
        self, client: ws_base.WebSocketClientBase, message: web_models.RoomBlockMessage
    ):
        """
        _on_room_block
        """

    #
    # 开放平台消息
    #

    def _on_open_live_danmaku(
        self, client: ws_base.WebSocketClientBase, message: open_models.DanmakuMessage
    ):
        """
        收到弹幕
        """

    def _on_open_live_gift(
        self, client: ws_base.WebSocketClientBase, message: open_models.GiftMessage
    ):
        """
        收到礼物
        """

    def _on_open_live_buy_guard(
        self, client: ws_base.WebSocketClientBase, message: open_models.GuardBuyMessage
    ):
        """
        有人上舰
        """

    def _on_open_live_super_chat(
        self, client: ws_base.WebSocketClientBase, message: open_models.SuperChatMessage
    ):
        """
        醒目留言
        """

    def _on_open_live_super_chat_delete(
        self,
        client: ws_base.WebSocketClientBase,
        message: open_models.SuperChatDeleteMessage,
    ):
        """
        删除醒目留言
        """

    def _on_open_live_like(
        self, client: ws_base.WebSocketClientBase, message: open_models.LikeMessage
    ):
        """
        点赞
        """
