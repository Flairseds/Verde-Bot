from resources.structures.Bloxlink import Bloxlink # pylint: disable=import-error


add_features = Bloxlink.get_module("utils", attrs=["add_features"])


@Bloxlink.command
class AddFeaturesCommand(Bloxlink.Module):
    """grant features to a user"""

    def __init__(self):
        self.arguments = [
            {
                "prompt": "Please specify the user or role(s) to grant features.",
                "name": "recipient",
                "type": "string",
            },
            {
                "prompt": "Please specify the features. Features: (premium, pro, -)",
                "name": "features",
                "type": "string",
            }
        ]
        self.category = "Developer"
        self.hidden = True
        self.developer = True
        self.aliases = ["add-features"]

    @Bloxlink.flags
    async def __main__(self, CommandArgs):
        message = CommandArgs.message
        response = CommandArgs.response

        features = CommandArgs.parsed_args["features"].replace(" ", "").split(",")

        try:
            days = int(CommandArgs.flags.get("days", 0))
        except ValueError:
            days = "-"

        premium_anywhere = bool(CommandArgs.flags.get("premium-anywhere", False))

        users = []

        for user in message.mentions:
            if not user.bot:
                users.append(user)

        for role in message.role_mentions:
            for member in role.members:
                if not member.bot:
                    users.append(member)


        for user in users:
            await add_features(user, features=features, days=days, premium_anywhere=premium_anywhere)

        await response.success(f"Successfully added features to **{len(users)}** user{len(users) > 1 and 's' or ''}!")