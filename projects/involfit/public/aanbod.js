const catalogue = document.querySelector('[data-catalogue]');
const tablist = catalogue.querySelector('nav');
const tabs = [...tablist.querySelectorAll('a')];
const panels = tabs.map(tab => document.querySelector(tab.hash));

tablist.setAttribute('role', 'tablist');
panels.forEach((panel, i) => {
  panel.setAttribute('role', 'tabpanel');
  panel.setAttribute('aria-labelledby', tabs[i].id);
  panel.tabIndex = 0;
  tabs[i].setAttribute('role', 'tab');
  tabs[i].setAttribute('aria-controls', panel.id);
});

function selectTab(index, {focus = false, updateUrl = false} = {}) {
  tabs.forEach((tab, i) => {
    tab.setAttribute('aria-selected', String(i === index));
    tab.tabIndex = i === index ? 0 : -1;
    panels[i].hidden = i !== index;
  });
  if (focus) tabs[index].focus();
  if (updateUrl && location.hash !== tabs[index].hash) {
    history.pushState(null, '', tabs[index].hash);
  }
}

function syncFromUrl() {
  selectTab(location.hash === '#trainingen' ? 1 : 0);
}

tabs.forEach((tab, index) => {
  tab.addEventListener('click', event => {
    event.preventDefault();
    selectTab(index, {focus: true, updateUrl: true});
  });
  tab.addEventListener('keydown', event => {
    const next = {
      Home: 0,
      End: tabs.length - 1,
      ArrowRight: (index + 1) % tabs.length,
      ArrowLeft: (index + tabs.length - 1) % tabs.length,
      ' ': index,
    }[event.key];
    if (next === undefined) return;
    event.preventDefault();
    selectTab(next, {focus: true, updateUrl: true});
  });
});
window.addEventListener('hashchange', syncFromUrl);
syncFromUrl();
