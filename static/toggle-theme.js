const UI_body = document.querySelector('body');
const UI_btn_themeChange = document.getElementById('theme-change-btn');
const getCurrentTheme = () => UI_body.classList.contains('dark') ? 'dark' : 'light';
const newTheme = () => getCurrentTheme() === 'dark' ? 'light' : 'dark';

function getThemeFromLocalStorage() {
    let theme = localStorage.getItem('sau-plants::theme');
    if (theme) {
        UI_body.classList.remove('dark', 'light');
        UI_body.classList.add(theme);
    } else {
        localStorage.setItem('sau-plants::theme', 'dark');
        UI_body.classList.add('dark');
    }
    updateThemeButton();
}

function updateThemeButton() {
    UI_btn_themeChange.firstElementChild.innerHTML = `${newTheme()}_mode`;
    UI_btn_themeChange.lastElementChild.innerHTML = newTheme();
}

function changeTheme() {
    localStorage.setItem('sau-plants::theme', newTheme());
    UI_body.classList.replace(getCurrentTheme(), newTheme());
    updateThemeButton();
}

window.onload = function () {
    getThemeFromLocalStorage();
}