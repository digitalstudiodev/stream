/**
 *  Light Switch @version v0.1.4
 */

(function () {
  let lightSwitch = document.getElementById('lightSwitch');
  if (!lightSwitch) {
    return;
  }

  /**
   * @function darkmode
   * @summary: changes the theme to 'dark mode' and save settings to local stroage.
   * Basically, replaces/toggles every CSS class that has '-light' class with '-dark'
   */
  function darkMode() {
    document.querySelectorAll('.bg-white').forEach((element) => {
      element.className = element.className.replace(/-white/g, '-dark');
    });

    document.querySelectorAll('.nav-light').forEach((element) => {
      element.className = element.className.replace(/-light/g, '-dark');
    });

    document.querySelectorAll('.link-dark').forEach((element) => {
      element.className = element.className.replace(/link-dark/, 'text-white');
    });


    document.body.classList.add('bg-dark');

    if (document.body.classList.contains('text-dark')) {
      document.body.classList.replace('text-dark', 'text-white');
    } else {
      document.body.classList.add('text-white');
    }

    document.querySelectorAll('.svg-border-rounded').forEach((element) => {
      element.className = element.className.replace(/text-white/, 'text-dark');
    });

    document.querySelectorAll('.nav-text').forEach((element) => {
      element.className = element.className.replace(/text-dark/, 'text-white');
    });

    document.querySelectorAll('.form-text').forEach((element) => {
      element.className = element.className.replace(/text-white/, 'text-dark');
    });

    document.querySelectorAll('.resume-text').forEach((element) => {
      element.className = element.className.replace(/text-white/, 'text-dark');
    });

    // Tables
    var tables = document.querySelectorAll('table');
    for (var i = 0; i < tables.length; i++) {
      // add table-dark class to each table
      tables[i].classList.add('table-dark');
    }

    // set light switch input to true
    if (!lightSwitch.checked) {
      lightSwitch.checked = true;
    }
    localStorage.setItem('lightSwitch', 'dark');
  }

  /**
   * @function lightmode
   * @summary: changes the theme to 'light mode' and save settings to local stroage.
   */
  function lightMode() {
    document.querySelectorAll('.bg-dark').forEach((element) => {
      element.className = element.className.replace(/-dark/g, '-white');
    });

    document.body.classList.add('bg-white');

    if (document.body.classList.contains('text-white')) {
      document.body.classList.replace('text-white', 'text-dark');
    } else {
      document.body.classList.add('text-dark');
    }

    document.querySelectorAll('.text-white').forEach((element) => {
      element.className = element.className.replace(/text-dark/, 'text-dark');
    });

    document.querySelectorAll('.svg-border-rounded').forEach((element) => {
      element.className = element.className.replace(/text-dark/, 'text-white');
    });

    document.querySelectorAll('.nav-text').forEach((element) => {
      element.className = element.className.replace(/text-white/, 'text-dark');
    });

    document.querySelectorAll('.form-text').forEach((element) => {
      element.className = element.className.replace(/text-white/, 'text-dark');
    });

    document.querySelectorAll('.resume-text').forEach((element) => {
      element.className = element.className.replace(/text-white/, 'text-dark');
    });

    // Tables
    var tables = document.querySelectorAll('table');
    for (var i = 0; i < tables.length; i++) {
      if (tables[i].classList.contains('table-dark')) {
        tables[i].classList.remove('table-dark');
      }
    }

    if (lightSwitch.checked) {
      lightSwitch.checked = false;
    }
    localStorage.setItem('lightSwitch', 'light');
  }

  /**
   * @function onToggleMode
   * @summary: the event handler attached to the switch. calling @darkMode or @lightMode depending on the checked state.
   */
  function onToggleMode() {
    if (lightSwitch.checked) {
      darkMode();
    } else {
      lightMode();
    }
  }

  /**
   * @function getSystemDefaultTheme
   * @summary: get system default theme by media query
   */
  function getSystemDefaultTheme() {
    const darkThemeMq = window.matchMedia('(prefers-color-scheme: dark)');
    if (darkThemeMq.matches) {
      return 'dark';
    }
    return 'white';
  }

  function setup() {
    var settings = localStorage.getItem('lightSwitch');
    if (settings == null) {
      settings = getSystemDefaultTheme();
    }

    if (settings == 'dark') {
      lightSwitch.checked = true;
    }

    lightSwitch.addEventListener('change', onToggleMode);
    onToggleMode();
  }

  setup();
})();