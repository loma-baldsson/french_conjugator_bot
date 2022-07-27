# French Verb Conjugator Discord Bot
#### Video Demo: https://youtu.be/aTPWXC7t9Fc
#### Description:
French Verbs are hard to conjugate, especially for those starting to learn it. I found verbs hard to conjugate so I wrote my own program to do it.

A conjugation is the resulting word produced by modifying a verb in accord to subject and tense.
For example, the conjugations of the verb "to be" at the present tense would be:
- I am
- You are
- He/she is
- We are
- You are
- They are

However, in French, this is much more complicated. See the conjugations for the equivilant verb, "être":
- Je suis
- Tu es
- Il/elle est
- Nous sommes
- Vous êtes
- Ils/elles sont

Since all French verbs follow a pattern for their conjugations, the program looks up the conjugation in a database and then formats it in a table. For example, the program would produce this text for the same tense and verb as the above:
```
INDICATIF PRÉSENT
┌─────────────┬────────────────┐
│ je suis     │ nous sommes    │
├─────────────┼────────────────┤
│ tu es       │ vous êtes      │
├─────────────┼────────────────┤
│ il/elle est │ ils/elles sont │
└─────────────┴────────────────┘
```
The source code is publicly available at https://github.com/loma-baldsson/french_conjugator_bot.

#### Usage:
You can run the command by sending `,conj VERB [TENSES]`, where `VERB` is the verb you want to conjugate (in the infinitive tense) and `TENSES` is an optional list of tenses that the bot should conjugate the verb in. By default, all tenses are output.
The tenses list is a list of short codes for each of the tenses. For example:
- Indicative: "i"
- Present Indicative: "ipr"
- Present Perfect Indicative: "ipc"

In addition, you can enable mobile mode by adding the `m` option.

#### Examples:
`,conj aimer ipr ipc` outputs the following:
```
INDICATIF PRÉSENT                      INDICATIF PASSÉ COMPOSÉ
┌──────────────┬──────────────────┐    ┌────────────────┬────────────────────┐
│ j'aime       │ nous aimons      │    │ j'ai aimé      │ nous avons aimé    │
├──────────────┼──────────────────┤    ├────────────────┼────────────────────┤
│ tu aimes     │ vous aimez       │    │ tu as aimé     │ vous avez aimé     │
├──────────────┼──────────────────┤    ├────────────────┼────────────────────┤
│ il/elle aime │ ils/elles aiment │    │ il/elle a aimé │ ils/elles ont aimé │
└──────────────┴──────────────────┘    └────────────────┴────────────────────┘
```

`,conj avoir ipr ipc m` outputs the following:
```
INDICATIF PRÉSENT
┌───────────┬───────────────┐
│ j'ai      │ nous avons    │
├───────────┼───────────────┤
│ tu as     │ vous avez     │
├───────────┼───────────────┤
│ il/elle a │ ils/elles ont │
└───────────┴───────────────┘
INDICATIF PASSÉ COMPOSÉ
┌──────────────┬──────────────────┐
│ j'ai eu      │ nous avons eu    │
├──────────────┼──────────────────┤
│ tu as eu     │ vous avez eu     │
├──────────────┼──────────────────┤
│ il/elle a eu │ ils/elles ont eu │
└──────────────┴──────────────────┘
```