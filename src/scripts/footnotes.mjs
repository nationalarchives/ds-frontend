const footnotePrefix = "footnote-";
const footnoteIdDataAttribute = "footnoteid";
const footnoteCitePrefix = "footnote-cite-";
const footnoteCiteIdDataAttribute = "footnoteid";
const $footnotes = document.getElementById("footnotes-list");
const $footnoteCites = Array.from(
  document.querySelectorAll(
    `[data-${footnoteCiteIdDataAttribute}]:has(a[href^="#${footnotePrefix}"])`,
  ),
);
/* eslint-disable-next-line no-secrets/no-secrets */
const letters = "abcdefghijklmnopqrstuvwxyz";

const footnoteCites = $footnoteCites.map(($footnoteCite) => ({
  $el: $footnoteCite,
  $link: $footnoteCite.querySelector("a"),
  id: $footnoteCite.dataset[footnoteCiteIdDataAttribute],
  group:
    $footnoteCites.findIndex(
      ($footnoteCiteEach) =>
        $footnoteCiteEach.dataset[footnoteCiteIdDataAttribute] ===
        $footnoteCite.dataset[footnoteCiteIdDataAttribute],
    ) + 1,
  instance: $footnoteCites
    .filter(
      ($footnoteCiteEach) =>
        $footnoteCiteEach.dataset[footnoteCiteIdDataAttribute] ===
        $footnoteCite.dataset[footnoteCiteIdDataAttribute],
    )
    .findIndex(($footnoteCiteEach) => $footnoteCiteEach === $footnoteCite),
}));

const footnotes = Array.from(
  $footnotes.querySelectorAll(`li[id^="${footnotePrefix}"]`),
)
  .map((footnote) => ({
    id: footnote.dataset[footnoteIdDataAttribute],
    html: footnote.innerHTML,
    firstInstance: footnoteCites.findIndex(
      (footnoteCite) => `${footnotePrefix}${footnoteCite.id}` === footnote.id,
    ),
  }))
  .sort((itemA, itemB) => {
    if (itemA.firstInstance === -1 && itemB.firstInstance === -1) {
      return 0;
    } else if (itemB.firstInstance === -1) {
      return -1;
    } else if (itemA.firstInstance === -1) {
      return 1;
    } else if (itemA.firstInstance < itemB.firstInstance) {
      return -1;
    } else if (itemA.firstInstance > itemB.firstInstance) {
      return 1;
    }
    return 0;
  });

footnoteCites.forEach((footnoteCite) => {
  const newId =
    footnotes.findIndex((footnote) => footnote.id === footnoteCite.id) + 1;
  footnoteCite.$link.innerText = `[${newId}]`;
  footnoteCite.$link.title = `See footnote ${newId}`;
  footnoteCite.$el.id = `${footnoteCitePrefix}${footnoteCite.group}${letters[footnoteCite.instance]}`;
});

$footnotes.innerHTML = footnotes.reduce(
  (html, footnote) =>
    `${html}<li id="${footnotePrefix}${footnote.id}">${footnoteCites.reduce(
      (footnoteCitesHtml, footnoteCite) =>
        footnoteCite.id === footnote.id
          ? `${footnoteCitesHtml}<a href="#${footnoteCitePrefix}${footnoteCite.group}${letters[footnoteCite.instance]}" title="Footnote ${footnoteCite.group}, cite ${letters[footnoteCite.instance]}">${letters[footnoteCite.instance]}</a> `
          : footnoteCitesHtml,
      "",
    )} <cite>${footnote.html}</cite></li>`,
  "",
);
