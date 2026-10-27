// Make Markdown task lists (- [ ]) tickable. State is kept per page in localStorage,
// so ticks survive reloads; it lives only in this browser.
(function () {
    var boxes = document.querySelectorAll('.content main li > input[type=checkbox][disabled]');
    if (!boxes.length) return;
    var key = 'checklist:' + location.pathname.replace(/^.*?\/(?=[^/]+\/[^/]+$|[^/]+$)/, '');
    var saved = [];
    try { saved = JSON.parse(localStorage.getItem(key)) || []; } catch (e) {}

    function save() {
        var state = Array.prototype.map.call(boxes, function (b) { return b.checked; });
        try { localStorage.setItem(key, JSON.stringify(state)); } catch (e) {}
    }

    boxes.forEach(function (box, i) {
        var li = box.parentElement;
        box.disabled = false;
        box.checked = !!saved[i];
        li.classList.add('task-item');
        li.classList.toggle('task-done', box.checked);
        box.addEventListener('change', function () {
            li.classList.toggle('task-done', box.checked);
            save();
        });
        // Clicking the item text toggles too (but not links inside it)
        li.addEventListener('click', function (e) {
            if (e.target === box || e.target.closest('a')) return;
            box.checked = !box.checked;
            box.dispatchEvent(new Event('change'));
        });
    });
})();
