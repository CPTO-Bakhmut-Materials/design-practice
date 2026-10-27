// Startup draw (lesson 1.5): random pick from the cards in #draw, shown as a slot-machine reel.
// One redraw is allowed; taken startups are remembered in this browser so a
// whole group can draw on one computer without repeats.
(function () {
    var root = document.getElementById('draw');
    if (!root) return;
    var $ = function (s) { return root.querySelector(s); };
    var cards = Array.prototype.map.call(root.querySelectorAll('.draw-list li'), function (li, i) {
        return { i: i, li: li, name: li.querySelector('b').textContent, desc: li.textContent.split(': ').slice(1).join(': '),
                 photos: li.getAttribute('data-photos') };
    });
    var card = $('.draw-card'), num = $('.draw-num'), strip = $('.draw-strip'), desc = $('.draw-desc');
    var go = $('.draw-go'), keep = $('.draw-keep'), redo = $('.draw-redo'), photos = $('.draw-photos');
    var KEY = 'startup-draw';
    var reduced = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
    var state = { taken: [], current: null, redrawn: false };
    try { state = Object.assign(state, JSON.parse(localStorage.getItem(KEY)) || {}); } catch (e) {}
    var spinning = false;

    function save() { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {} }

    function pool(except) {
        return cards.filter(function (c) { return state.taken.indexOf(c.i) < 0 && c.i !== except; });
    }

    function rows(list) {
        strip.innerHTML = '';
        list.forEach(function (c) {
            var r = document.createElement('div');
            r.className = 'draw-row';
            r.textContent = typeof c === 'string' ? c : c.name;
            strip.appendChild(r);
        });
    }

    function rowHeight() { return strip.firstChild ? strip.firstChild.offsetHeight : 64; }

    var at = 1;  // strip row currently in the middle

    // Put row `i` of the strip in the middle of the 3-row window
    function centre(i, animate, done) {
        at = i;
        strip.style.transition = animate ? 'transform 3.8s cubic-bezier(.15, .55, .12, 1)' : 'none';
        strip.style.transform = 'translateY(' + (-(i - 1) * rowHeight()) + 'px)';
        if (!animate) return done && done();
        var fired = false;
        function end() { if (!fired) { fired = true; done(); } }
        strip.addEventListener('transitionend', end, { once: true });
        setTimeout(end, 4300);
    }

    function random(except) {
        var c;
        do { c = cards[Math.floor(Math.random() * cards.length)]; } while (c === except);
        return c;
    }

    function idle() {
        num.textContent = '?';
        desc.textContent = 'Натисніть «Тягнути картку»';
        rows([random(), 'Ваш стартап', random()]);
        centre(1);
    }

    function label(c) {
        num.textContent = String(c.i + 1).padStart(2, '0');
        desc.textContent = c.desc;
    }

    function show(c) {
        label(c);
        rows([random(c), c, random(c)]);
        centre(1);
    }

    function render() {
        cards.forEach(function (c) { c.li.classList.toggle('draw-taken', state.taken.indexOf(c.i) >= 0); });
        var deciding = state.current !== null;
        var left = pool().length;
        go.hidden = deciding;
        keep.hidden = !deciding;
        redo.hidden = !deciding || state.redrawn || pool(state.current).length === 0;
        go.disabled = left === 0;
        go.textContent = left === 0 ? 'Картки закінчилися' : state.taken.length ? 'Тягнути для наступного' : 'Тягнути картку';
    }

    function showPhotos(c) {
        photos.hidden = false;
        photos.innerHTML = 'Фото для вашої теми: <a href="materialy.html#photos-' + c.photos + '"><code>brand-day/photos/' +
            c.photos + '/</code></a>';
    }

    // Reel: the rows now on screen, ~40 random names, then the target and one more below it
    function spin(target, done) {
        spinning = true;
        card.classList.remove('draw-win');
        photos.hidden = true;
        num.textContent = '…';
        desc.textContent = '\u00a0';
        var seq = Array.prototype.slice.call(strip.children, at - 1, at + 2).map(function (r) { return r.textContent; });
        var prev = null;
        for (var k = 0; k < 40; k++) { prev = random(prev); seq.push(prev); }
        seq.push(target, random(target));
        rows(seq);
        centre(1);
        void strip.offsetWidth;  // apply the start position before animating
        var landed = function () {
            card.classList.remove('draw-spinning');
            label(target);  // the strip stays where it stopped
            void card.offsetWidth;  // restart the landing animation
            card.classList.add('draw-win');
            spinning = false;
            done();
        };
        if (reduced) { centre(seq.length - 2); return landed(); }
        card.classList.add('draw-spinning');
        setTimeout(function () { card.classList.remove('draw-spinning'); }, 2600);
        centre(seq.length - 2, true, landed);
    }

    function draw(except) {
        var from = pool(except);
        if (spinning || !from.length) return;
        var target = from[Math.floor(Math.random() * from.length)];
        go.disabled = keep.disabled = redo.disabled = true;
        spin(target, function () {
            go.disabled = keep.disabled = redo.disabled = false;
            state.current = target.i;
            if (except !== undefined) { state.redrawn = true; }
            save();
            if (state.redrawn) return take();  // the redraw is final
            render();
        });
    }

    function take() {
        var c = cards[state.current];
        state.taken.push(c.i);
        state.current = null;
        state.redrawn = false;
        save();
        showPhotos(c);
        render();
    }

    go.addEventListener('click', function () { draw(); });
    redo.addEventListener('click', function () { draw(state.current); });
    keep.addEventListener('click', take);
    $('.draw-reset').addEventListener('click', function () {
        if (!confirm('Почати жеребкування заново? Список взятих стартапів очиститься.')) return;
        state = { taken: [], current: null, redrawn: false };
        save();
        idle();
        card.classList.remove('draw-win'); photos.hidden = true;
        render();
    });

    root.classList.add('draw-ready');
    if (state.current !== null && cards[state.current]) { show(cards[state.current]); card.classList.add('draw-win'); }
    else idle();
    render();
})();
