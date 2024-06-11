import asyncio

from datetime import datetime
from nextcord import AuditLogAction, Forbidden, Member


class Invite:

    def __init__(self, bot) -> None:
        self.bot = bot
        self._data= {}
        self.add_listeners()

    def add_listeners(self):
        self.bot.add_listener(self.invites_data, "on_ready")
        self.bot.add_listener(self.update_invite_data, "on_invite_create")
        self.bot.add_listener(self.remove_invite_data, "on_invite_delete")

    async def invites_data(self):
        for guild in self.bot.guilds:
            self._data[guild.id] = {}
            for invite in await guild.invites():
                self._data[guild.id][invite.code] = invite

    async def update_invite_data(self, invite):
        self._data[invite.guild.id][invite.code] = invite

    async def remove_invite_data(self, invite):
        ref_invite = self._data[invite.guild.id][invite.code]

        current_time = datetime.now().timestamp()
        invite_creation_time = ref_invite.created_at.timestamp()

        is_valid_time = (invite_creation_time + ref_invite.max_age > current_time or ref_invite.max_age == 0)
        is_uses_left = ref_invite.uses == ref_invite.max_uses - 1
        is_still_valid = ref_invite.max_uses > 0

        if is_valid_time and is_still_valid and is_uses_left:
            try:
                async for entry in invite.guild.audit_logs(limit=1, action=AuditLogAction.invite_delete):
                    if entry.target.code != invite.code:
                        self._data[invite.guild.id][ref_invite.code].revoked = True
                        ref_invite
                    else:
                        self._data[invite.guild.id][ref_invite.code].revoked =True
                        ref_invite
        
            except Forbidden:
                self._data[invite.guild.id][ref_invite.code].revoked = True
                ref_invite
        else:
            self._data[invite.guild.id].pop(invite.code)

    async def fetch_inviter(self, member: Member):
        await asyncio.sleep(self.bot.latency)

        for new_invite in await member.guild.invites():
            for invites_data in self._data[member.guild.id].values():

                if new_invite.code == invites_data.code and new_invite.uses - invites_data.uses  == 1 or invites_data.revoked:
                    if invites_data.revoked:
                        self._data[member.guild.id].pop(invites_data.code)
                    elif new_invite.inviter == invites_data.inviter:
                        self._data[member.guild.id][invites_data.code] = new_invite
                    else:
                        self._data[member.guild.id][invites_data.code].uses += 1
                    
                    return invites_data.code, invites_data.inviter
