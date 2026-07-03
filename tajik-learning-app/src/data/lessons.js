// Дарсҳои грамматикаи забони англисӣ (сатҳи A1–A2), шарҳ бо забони тоҷикӣ
export const LESSONS = [
  {
    id: "present-simple",
    title: "Present Simple",
    subtitle: "Замони ҳозираи одӣ",
    explanation:
      "Present Simple барои ифодаи амали доимӣ, одат ё далели умумӣ истифода мешавад. Мисол: I work, she works. Бо шахси саввуми танҳо (he/she/it) ба феъл -s ё -es илова мешавад.",
    questions: [
      { q: "She ___ (work) every day.", options: ["work", "works", "working"], answer: "works" },
      { q: "I ___ (live) in Dushanbe.", options: ["lives", "live", "living"], answer: "live" },
      { q: "They ___ (not / like) coffee.", options: ["doesn't like", "don't like", "not like"], answer: "don't like" },
    ],
  },
  {
    id: "past-simple",
    title: "Past Simple",
    subtitle: "Замони гузаштаи одӣ",
    explanation:
      "Past Simple амали дар гузашта анҷомёфтаро ифода мекунад. Феълҳои қоидавӣ -ed мегиранд (work → worked), аммо феълҳои номунтазам шакли махсус доранд (go → went).",
    questions: [
      { q: "Yesterday I ___ (go) to school.", options: ["go", "went", "gone"], answer: "went" },
      { q: "She ___ (buy) a new book last week.", options: ["buy", "bought", "buys"], answer: "bought" },
      { q: "We ___ (not / see) him yesterday.", options: ["didn't saw", "didn't see", "not saw"], answer: "didn't see" },
    ],
  },
  {
    id: "present-continuous",
    title: "Present Continuous",
    subtitle: "Замони ҳозираи давомдор",
    explanation:
      "Present Continuous барои амале, ки ҳозир рӯй медиҳад, истифода мешавад: am/is/are + феъл-ing. Мисол: I am reading a book now.",
    questions: [
      { q: "He ___ (read) a book now.", options: ["is reading", "reads", "read"], answer: "is reading" },
      { q: "We ___ (watch) TV at the moment.", options: ["are watching", "watch", "watched"], answer: "are watching" },
      { q: "___ you ___ (listen) to me?", options: ["Are / listening", "Do / listen", "Is / listen"], answer: "Are / listening" },
    ],
  },
  {
    id: "articles",
    title: "Articles: a / an / the",
    subtitle: "Артикльҳо",
    explanation:
      "'A' пеш аз садоноки ҳамсадо истифода мешавад (a book), 'an' пеш аз садои садонок (an apple). 'The' барои чизи мушаххас ё маълум истифода мешавад.",
    questions: [
      { q: "I have ___ apple.", options: ["a", "an", "the"], answer: "an" },
      { q: "Look at ___ sun — it's very bright today.", options: ["a", "an", "the"], answer: "the" },
      { q: "She is ___ teacher.", options: ["a", "an", "the"], answer: "a" },
    ],
  },
  {
    id: "plural-nouns",
    title: "Plural Nouns",
    subtitle: "Ҷамъбандии исмҳо",
    explanation:
      "Аксарияти исмҳо бо илова кардани -s ҷамъ мешаванд (book → books). Баъзеашон истисноанд: child → children, man → men, woman → women.",
    questions: [
      { q: "One book, two ___.", options: ["book", "books", "bookes"], answer: "books" },
      { q: "One child, two ___.", options: ["childs", "children", "childes"], answer: "children" },
      { q: "One woman, two ___.", options: ["womans", "women", "womens"], answer: "women" },
    ],
  },
  {
    id: "question-words",
    title: "Question Words",
    subtitle: "Калимаҳои саволӣ",
    explanation:
      "What (чӣ), where (куҷо), when (кай), who (кӣ), why (чаро), how (чӣ тавр) — барои сохтани саволҳо истифода мешаванд.",
    questions: [
      { q: "___ is your name?", options: ["What", "Where", "When"], answer: "What" },
      { q: "___ do you live?", options: ["Who", "Where", "Why"], answer: "Where" },
      { q: "___ are you late?", options: ["How", "Why", "Who"], answer: "Why" },
    ],
  },
];
