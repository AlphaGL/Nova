// static/js/script.js

document.addEventListener('DOMContentLoaded', function() {
    // --- Theme and Customization ---
    const themeRadios = document.querySelectorAll('input[name="theme"]');
    const customOptions = document.getElementById('custom-theme-options');
    const bgColorInput = document.getElementById('bgColor');
    const textColorInput = document.getElementById('textColor');
    const fontSelect = document.getElementById('fontSelect');

    // Load saved preferences or defaults
    let theme = localStorage.getItem('theme') || 'light';
    let bgColor = localStorage.getItem('bgColor') || '#ffffff';
    let textColor = localStorage.getItem('textColor') || '#000000';
    let font = localStorage.getItem('font') || 'Arial';

    // Apply theme styles
    applyTheme(bgColor, textColor, font);

    // Set UI controls to current values
    document.getElementById('theme-' + theme)?.checked = true;
    if (theme === 'custom') customOptions.style.display = 'block';
    bgColorInput.value = bgColor;
    textColorInput.value = textColor;
    fontSelect.value = font;

    // Theme selection change
    themeRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            const selected = this.value;
            localStorage.setItem('theme', selected);
            if (selected === 'custom') {
                customOptions.style.display = 'block';
                // Use existing custom colors
                applyTheme(localStorage.getItem('bgColor'), localStorage.getItem('textColor'), localStorage.getItem('font'));
            } else {
                customOptions.style.display = 'none';
                if (selected === 'light') {
                    bgColor = '#ffffff'; textColor = '#000000';
                } else if (selected === 'dark') {
                    bgColor = '#000000'; textColor = '#ffffff';
                }
                // Save defaults for light/dark
                localStorage.setItem('bgColor', bgColor);
                localStorage.setItem('textColor', textColor);
                bgColorInput.value = bgColor;
                textColorInput.value = textColor;
                applyTheme(bgColor, textColor, fontSelect.value);
            }
        });
    });

    // Background color change
    bgColorInput.addEventListener('input', function() {
        localStorage.setItem('bgColor', this.value);
        applyTheme(this.value, localStorage.getItem('textColor'), fontSelect.value);
    });

    // Text color change
    textColorInput.addEventListener('input', function() {
        localStorage.setItem('textColor', this.value);
        applyTheme(localStorage.getItem('bgColor'), this.value, fontSelect.value);
    });

    // Font selection change
    fontSelect.addEventListener('change', function() {
        localStorage.setItem('font', this.value);
        applyTheme(localStorage.getItem('bgColor'), localStorage.getItem('textColor'), this.value);
    });

    // Apply theme by setting body styles
    function applyTheme(bg, text, font) {
        document.body.style.backgroundColor = bg;
        document.body.style.color = text;
        document.body.style.fontFamily = font;
    }

    // --- Recent Searches ---
    const recentDiv = document.getElementById('recent-searches');
    const params = new URLSearchParams(window.location.search);
    const currentQuery = params.get('q');

    if (recentDiv) {
        let searches = JSON.parse(localStorage.getItem('recentSearches') || '[]');
        if (currentQuery) {
            // Remove if exists and then add to front
            searches = searches.filter(item => item !== currentQuery);
            searches.unshift(currentQuery);
            if (searches.length > 5) searches.pop();
            localStorage.setItem('recentSearches', JSON.stringify(searches));
        }
        if (searches.length > 0) {
            let html = '<h5>Recent Searches:</h5><ul class="ps-0">';
            searches.forEach(item => {
                html += `<li><a href="?q=${encodeURIComponent(item)}">${item}</a></li>`;
            });
            html += '</ul>';
            recentDiv.innerHTML = html;
        }
    }
});
