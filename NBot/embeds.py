import discord
from datetime import datetime

def standard_embed(text):
    """
    Returns a discord embed with a basic textual inclusion
    :param text:
    :return:
    """
    base = discord.Embed(
        description=text,
        colour=discord.Colour.og_blurple()
    )
    base.set_footer(text=datetime.now())
    return base


def expenses_embed(expense_list):
    """
    Returns a discord embed structuring a specific expense dataset:

    Dataset example:
        [ ["Saving", "100%", "$1,054.04", "$2234.03"],
          ["Dining", "Percentage", "Used", "Allowance"],
        ]

    :param expenses_dict: list of lists involving data from expense sheet
    :return:
    """
    base = discord.Embed(
        description="Expense Report",
        colour=discord.Colour.brand_green()
    )

    base.add_field(name=f'**__Saving__**',
                   value=f"Total: {expense_list[0][2]}",
                   inline=True)

    for i, expense_item in enumerate(expense_list):
        if i == 0:  # Skip saving data, handled by first field
            continue

        base.add_field(name=f"**__{expense_item[0]}__**",
                       value=f"{expense_item[1]}\n"
                             f"*{expense_item[2]}/{expense_item[3]}*",
                       inline=True)
    base.set_footer(text=datetime.now())

    return base

