"""Get all Users in Discord Command"""
from src.settings import MOD, ALL_USERS, MOD_PERMISSIONS
from src.mentor_roles import MentorRoles
from commands.base_command import BaseCommand
import database.database as db

class GetUsers(BaseCommand):
    """Get users class"""
    def __init__(self):
        description = 'Get all users and add to database for SOTW/BOTW'
        super().__init__(description, None, MOD)

    def set_mentor_content(self, username):
        """Set content which mentor user will be added to database"""
        is_consultant = False

        if 'mr skeng man' in username:
            content_names = MentorRoles.COX['name'],MentorRoles.GWD['name']
            content_names = ','.join(content_names)
            return {
                'content': content_names,
                'consultant': is_consultant
            }
        if 'EastonKnows' in username:
            content_names = MentorRoles.COX['name'],MentorRoles.TOB['name']
            content_names = ','.join(content_names)
            is_consultant = True
            return {
                'content': content_names,
                'consultant': is_consultant
            }
        if 'Hobo UwUber' in username:
            content_names = MentorRoles.COX['name'], \
                MentorRoles.SOLO_COX['name'], MentorRoles.INFERNO['name'], \
                    MentorRoles.ZULRAH['name']
            content_names = ','.join(content_names)
            return {
                'content': content_names,
                'consultant': is_consultant
            }
        if 'Ruto' in username:
            is_consultant = True
            content_names = MentorRoles.COX['name'], \
                MentorRoles.SOLO_COX['name'], MentorRoles.GENERAL_PVM['name']
            content_names = ','.join(content_names)
            return {
                'content': content_names,
                'consultant': is_consultant
            }
        if 'x Dodgy x' in username:
            content_names = MentorRoles.TOB['name'],MentorRoles.INFERNO['name']
            content_names = ','.join(content_names)
            return {
                'content': content_names,
                'consultant': is_consultant
            }
        if 'ITIagicks' in username:
            content_names = MentorRoles.VORKATH['name'], \
                MentorRoles.SEPULCHRE['name'], MentorRoles.GENERAL_PVM['name']
            content_names = ','.join(content_names)
            is_consultant = True
            return {
                'content': content_names,
                'consultant': is_consultant
            }
        if 'Ethan' in username:
            is_consultant = True
            content_names = MentorRoles.COX['name'],MentorRoles.TOB['name'], \
                MentorRoles.GAUNTLET['name'],MentorRoles.GENERAL_PVM['name']
            content_names = ','.join(content_names)
            return {
                'content': content_names,
                'consultant': is_consultant
            }
        return None

    async def handle(self, params, message, client):
        """Handle command"""
        print(message.channel.name)
        for guild in client.guilds:
            print('guild', guild)
            if str(guild) != 'Horro':
                for member in guild.members:
                    if '🤝Verified' in str(member.top_role):
                        continue
                    if '🤖 Bots' in str(member.top_role):
                        continue
                    else:
                        role = (str(member.top_role))
                        if role in MOD_PERMISSIONS:
                            permissions = MOD
                        else:
                            permissions = ALL_USERS
                        print(f'Name: {member.display_name} \nPermissions: \
                            {permissions}\nRole: {member.top_role}')
                        print(f'Roles: {member.roles}')
                        role_names = list(map(lambda n: n.name, member.roles))
                        role_names = ','.join(role_names)
                        consultant = False
                        content = None
                        if 'Mentor' in role_names:
                            content_dict = self.set_mentor_content(\
                                member.display_name)
                            print(f'Content: {content_dict}')
                            if content_dict is not None:
                                content = content_dict['content']
                                consultant = content_dict['consultant']
                        db.insert_members(str(member.id), \
                            str(member.display_name), str(member.top_role), \
                                permissions, role_names, content, consultant)

        # display_name, top_role, id, permissions, roles
        guilds = await client.fetch_guilds(limit=150).flatten()
        print(guilds)
        await message.channel.send('success')
