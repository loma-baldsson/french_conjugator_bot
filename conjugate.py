import discord
import os
import conjugate
import table_creator
import pprint

PRONOUNS = ["je", "tu", "il/elle", "nous", "vous", "ils/elles"]
SUBJECT_TENSES = ["SUBJONCTIF", "INDICATIF", "CONDITIONNEL"]

ALIASES = {
    "SUBJONCTIF": ["s"],
    "INDICATIF": ["i"],
    "CONDITIONNEL": ["c"],
    "IMPÉRATIF": ["im"],
    "INFINITIF": ["in"],
    "PARTICIPE": ["p"],

    "INDICATIF PRÉSENT": ["ipr"],
    "INDICATIF IMPARFAIT": ["iim"],
    "INDICATIF PASSÉ SIMPLE": ["ips"],
    "INDICATIF FUTUR SIMPLE": ["ifs"],
    "INDICATIF PASSÉ COMPOSÉ": ["ipc"],
    "INDICATIF PLUS-QUE-PARFAIT": ["ipp"],
    "INDICATIF PASSÉ ANTÉRIEUR": ["ipa"],
    "INDICATIF FUTUR ANTÉRIEUR": ["ifa"],

    "SUBJONCTIF PRÉSENT": ["spr"],
    "SUBJONCTIF IMPARFAIT": ["sim"],
    "SUBJONCTIF PASSÉ": ["spc"],
    "SUBJONCTIF PLUS-QUE-PARFAIT": ["spp"],

    "CONDITIONNEL PRÉSENT": ["cpr"],
    "CONDITIONNEL PASSÉ": ["cpr"],

    "IMPÉRATIF PRÉSENT": ["impr"],
    "IMPÉRATIF PASSÉ": ["impc"],

    "INFINITIF PRÉSENT": ["inpr"],
    "INFINITIF PASSÉ": ["inpc"],

    "PARTICIPE PRÉSENT": ["ppr"],
    "PARTICIPE PASSÉ": ["ppa"],
}

client = discord.Client()
rows = conjugate.load_file()

def add_pronouns(tense, conjugations):
    if tense.split(" ")[0] in SUBJECT_TENSES:
        for index, conjugation in enumerate(conjugations):
            if conjugation != "":
                if index == 0:
                    if conjugation[0] in ["a", "e", "i", "o", "u"]:
                        conjugations[index] = f"j'{conjugation}"
                    else:
                        conjugations[index] = f"je {conjugation}"
                else:
                    conjugations[index] = f"{PRONOUNS[index]} {conjugation}"

    return conjugations

def create_conjugation_tables(verb, tables_per_row=2, allowed_tenses="ALL"):
    assert type(verb) == str, "Verb is not a string"
    assert type(tables_per_row) == int, "tables_per_row is not an int"
    assert type(allowed_tenses) == list or allowed_tenses == "ALL", "conjugations is neither list nor 'all'"

    all_conjugations = []

    for tense in conjugate.TENSES:
        can_continue = False

        if allowed_tenses != "ALL":
            for allowed_tense in allowed_tenses:
                print(allowed_tense, tense.find(allowed_tense))
                if tense.find(allowed_tense) != -1:
                    can_continue = True
        else:
            can_continue = True

        if not can_continue:
            continue

        conjugations = conjugate.conjugate(rows, verb, tense)

        pronoun_conjugations = add_pronouns(tense, conjugations)
        formatted_conjugations = []

        if len(pronoun_conjugations) == 6:
            for i in range(3):
                formatted_conjugations.append([pronoun_conjugations[i], pronoun_conjugations[i+3]])
        else:
            formatted_conjugations.append([pronoun_conjugations[0]])

        formatted_conjugations.insert(0, tense)

        all_conjugations.append(formatted_conjugations)

    conjugation_tables = []
    padding = 0

    for index, conjugation in enumerate(all_conjugations):
        table = table_creator.render_table(conjugation[1:])
        table_length = len(table.split("\n")[1])
        padding = max(padding, table_length)

        new_table = table_creator.pad_table(f"{conjugation[0]}\n{table}")

        conjugation_tables.append(new_table)

    rendered_tables = []

    for i in range(0, len(conjugation_tables), tables_per_row):
        tables = []
        for j in range(tables_per_row):
            try:
                tables.append(conjugation_tables[i+j])
            except IndexError:
                pass

        padding_required = padding - len(tables[0].split("\n")[0])

        rendered_tables.append(table_creator.join_tables(*tables, padding=padding_required))

    return rendered_tables

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(",hello"):
        await message.channel.send(f"world")

    if message.content.startswith(",conj") and len(message.content.split()) == 1:
        await message.channel.send(f"Usage: `,conj VERB [TENSES]`")

    if message.content.startswith(",conj") and len(message.content.split()) > 1:
        options = message.content.split()[2:]

        if "m" in options:
            cols = 1
            options.remove("m")
        else:
            cols = 2

        for index, alias in enumerate(options):
            for tense, tense_aliases in ALIASES.items():
                if alias.lower() in tense_aliases:
                    options[index] = tense

        if len(options) == 0:
            options = "ALL"

        rendered_tables = create_conjugation_tables(message.content.split()[1], cols, options)

        curr_msg = ""
        for index, row in enumerate(rendered_tables):
            if len(curr_msg + row) > 2000:
                await message.channel.send(f"```{curr_msg}```")
                curr_msg = ""

            curr_msg += row
            curr_msg += "\n"

            if index == len(rendered_tables)-1:
                await message.channel.send(f"```{curr_msg}```")


client.run(os.environ["DISCORD_BOT_TOKEN"])
