"""
Instantiates the Discord Bot
Holds bot functions
"""

# Imports
import json
from discord.ext import commands
import discord
import os
import platform
import embeds
import googlesheetservice as gss

# Bot instance
bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

# Load bot configuration file
with open("config.json", "r") as f:
    config = json.load(f)


# On Ready Data
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")


# BUDGET COMMANDS
# ______________________________________________________________________________________________________________________


def expense(category: str, amount: float, note: str = None):
    """
    Verifies the expense category and a numerical value, manages googlesheetservice connection to expense update
    requests in budget commands
    :param category: Required contextual argument from discord.py message
    :param amount: Value to update expense with (dollar value, i.e. 5 or 5.23)
    :param note: A note to add to the spreadsheet cell, defaults to nothing
    """
    if category not in ['Dining', 'Grocery', 'Transportation', 'Recreation', 'Personal', 'JL', 'Other']:
        print(f"'{category}' was not found to be a proper category")
        return 0

    try:
        amount = float(amount)
    except ValueError:
        print(f"'{amount}' is not a valid number")
        return 0

    return gss.add_expense(category, amount, note)


@bot.command(aliases=["din"])
async def dining_expense(ctx, *args):
    """
    Adds a mentioned expense value to the "Dining" expense category list in the N-Fam Google spreadsheets
    :param ctx: Standard required discord contextual argument, autofill by discord api
    :param args: List of arguments, initial argument must be numerical dollar value,
                 optional second argument for an expense note
    """
    if len(args) > 1:
        result = expense("Dining", args[0], args[1])
    else:
        result = expense("Dining", args[0])

    if result:
        amount = float(args[0])
        await ctx.send(
            embed=embeds.standard_embed(text=f'${amount:.2f} was added to dining expenses'))
        return

    await ctx.send(
        embed=embeds.standard_embed(text="Sorry, something went wrong")
    )


@bot.command(aliases=["gro"])
async def grocery_expense(ctx, *args):
    """
    Adds a mentioned expense value to the "Grocery" expense category list in the N-Fam Google spreadsheets
    :param ctx: Standard required discord contextual argument, autofill by discord api
    :param args: List of arguments, initial argument must be numerical dollar value,
                 optional second argument for an expense note
    """
    if len(args) > 1:
        result = expense("Grocery", args[0], args[1])
    else:
        result = expense("Grocery", args[0])

    if result:
        amount = float(args[0])
        await ctx.send(
            embed=embeds.standard_embed(text=f'${amount:.2f} was added to grocery expenses'))
        return

    await ctx.send(
        embed=embeds.standard_embed(text="Sorry, something went wrong")
    )


@bot.command(aliases=["tra"])
async def transportation_expense(ctx, *args):
    """
    Adds a mentioned expense value to the "Transportation" expense category list in the N-Fam Google spreadsheets
    :param ctx: Standard required discord contextual argument, autofill by discord api
    :param args: List of arguments, initial argument must be numerical dollar value,
                 optional second argument for an expense note
    """
    if len(args) > 1:
        result = expense("Transportation", args[0], args[1])
    else:
        result = expense("Transportation", args[0])

    if result:
        amount = float(args[0])
        await ctx.send(
            embed=embeds.standard_embed(text=f'${amount:.2f} was added to transportation expenses'))
        return

    await ctx.send(
        embed=embeds.standard_embed(text="Sorry, something went wrong")
    )


@bot.command(aliases=["rec"])
async def recreation_expense(ctx, *args):
    """
    Adds a mentioned expense value to the "Recreation" expense category list in the N-Fam Google spreadsheets
    :param ctx: Standard required discord contextual argument, autofill by discord api
    :param args: List of arguments, initial argument must be numerical dollar value,
                 optional second argument for an expense note
    """
    if len(args) > 1:
        result = expense("Recreation", args[0], args[1])
    else:
        result = expense("Recreation", args[0])

    if result:
        amount = float(args[0])
        await ctx.send(
            embed=embeds.standard_embed(text=f'${amount:.2f} was added to recreation expenses'))
        return

    await ctx.send(
        embed=embeds.standard_embed(text="Sorry, something went wrong")
    )


@bot.command(aliases=["per"])
async def personal_expense(ctx, *args):
    """
    Adds a mentioned expense value to the "Personal" expense category list in the N-Fam Google spreadsheets
    :param ctx: Standard required discord contextual argument, autofill by discord api
    :param args: List of arguments, initial argument must be numerical dollar value,
                 optional second argument for an expense note
    """
    if len(args) > 1:
        result = expense("Personal", args[0], args[1])
    else:
        result = expense("Personal", args[0])

    if result:
        amount = float(args[0])
        await ctx.send(
            embed=embeds.standard_embed(text=f'${amount:.2f} was added to personal expenses'))
        return

    await ctx.send(
        embed=embeds.standard_embed(text="Sorry, something went wrong")
    )


@bot.command(aliases=["jl"])
async def jl_expense(ctx, *args):
    """
    Adds a mentioned expense value to the "JL" expense category list in the N-Fam Google spreadsheets
    :param ctx: Standard required discord contextual argument, autofill by discord api
    :param args: List of arguments, initial argument must be numerical dollar value,
                 optional second argument for an expense note
    """
    if len(args) > 1:
        result = expense("JL", args[0], args[1])
    else:
        result = expense("JL", args[0])

    if result:
        amount = float(args[0])
        await ctx.send(
            embed=embeds.standard_embed(text=f'${amount:.2f} was added to Jett and Lennox expenses'))
        return

    await ctx.send(
        embed=embeds.standard_embed(text="Sorry, something went wrong")
    )


@bot.command(aliases=["oth"])
async def other_expense(ctx, *args):
    """
    Adds a mentioned expense value to the "Other" expense category list in the N-Fam Google spreadsheets
    :param ctx: Standard required discord contextual argument, autofill by discord api
    :param args: List of arguments, initial argument must be numerical dollar value,
                 optional second argument for an expense note
    """
    if len(args) > 1:
        result = expense("Other", args[0], args[1])
    else:
        result = expense("Other", args[0])

    if result:
        amount = float(args[0])
        await ctx.send(
            embed=embeds.standard_embed(text=f'${amount:.2f} was added to other expenses'))
        return

    await ctx.send(
        embed=embeds.standard_embed(text="Sorry, something went wrong")
    )


@bot.command(aliases=["expenses"])
async def expense_chart(ctx):
    """
    Displays all expense data - percentage, usage, and allowance
    :param ctx: Standard required discord contextual argument, autofill by discord api
    """
    result = gss.get_all_expense_data()
    if result:
        await ctx.send(
            embed=embeds.expenses_embed(result)
        )


@bot.command(aliases=["cinc"])
async def cody_income(ctx, amount):
    """
    Sets or accumulates income for Cody in budget spreadsheet, replies with a discord message on success
    :param ctx: Standard required discord contextual argument, autofill by discord api
    :param amount: String numerical value to add to Cody's income
    """
    try:
        amount = float(amount)
    except ValueError:
        await ctx.send(embed=embeds.standard_embed(text="Sorry, something went wrong"))

    if gss.get_income_total("Cody"):  # Cumulate an already present income
        gss.cumulate_dollar_format_cell(amount, "C59")
        await ctx.send(embed=embeds.standard_embed(text="Cody's income has been updated!"))

    else:
        gss.update_income("Cody", amount)  # Put income into an empty cell
        await ctx.send(embed=embeds.standard_embed(text="Cody's income has been updated!"))


@bot.command(aliases=["sinc"])
async def sam_income(ctx, amount):
    """
    Sets or accumulates income for Cody in budget spreadsheet. Replies with a discord message on success
    :param ctx: Standard required discord contextual argument, autofill by discord api
    :param amount: String numerical value to add to Sam's income.
    """
    try:
        amount = float(amount)
    except ValueError:
        await ctx.send(embed=embeds.standard_embed(text="Sorry, something went wrong"))

    if gss.get_income_total("Sam"):  # Cumulate an already present income
        gss.cumulate_dollar_format_cell(amount, "C60")
        await ctx.send(embed=embeds.standard_embed(text="Sam's income has been updated!"))

    else:
        gss.update_income("Sam", amount)  # Put income into an empty cell
        await ctx.send(embed=embeds.standard_embed(text="Sam's income has been updated!"))


@bot.command(aliases=["oinc"])
async def other_income(ctx, amount):
    """
    Sets or accumulates income for Cody in budget spreadsheet.
    :param ctx: Standard required discord contextual argument, autofill by discord api
    :param amount: String numerical value to add to income.
    :return:
    """
    try:
        amount = float(amount)
    except ValueError:
        await ctx.send(embed=embeds.standard_embed(text="Sorry, something went wrong"))

    if gss.get_income_total("Other"):  # Cumulate an already present income
        gss.cumulate_dollar_format_cell(amount, "C61")
        await ctx.send(embed=embeds.standard_embed(text="Other income has been updated!"))

    else:
        gss.update_income("Other", amount)  # Put income into an empty cell
        await ctx.send(embed=embeds.standard_embed(text="Other income has been updated!"))


# END BUDGET COMMANDS
# ______________________________________________________________________________________________________________________

bot.run(config["token"])