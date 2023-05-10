let qs = (e) => document.querySelector(e);
let qsa = (e) => document.querySelectorAll(e);

document.addEventListener('DOMContentLoaded', () => {
    // Const variables
    const h_calcs = qsa('.h-calc');

    const epic_gradient = qsa('.epic_gradient');
    const epic_bg = qsa('.epic_bg');

    const menuBtn = qs(".epic_menu-btn");
    const closeMenuBtn = qs(".epic_close-nav");
    const copyBtns = qsa(".epic_copy-btns");

    const observe_anim = qsa('.observe_anim');
 
    // Event Listeners
    if (menuBtn != null) {
        menuBtn.addEventListener("click", dropmenu);
        closeMenuBtn.addEventListener("click", dropmenu);
    }

    // For Each Functions
    h_calcs.forEach(e => {
        if (e.clientWidth > 768) {
            let tall = e.offsetHeight;
            e.style.height = tall + 'px' 
        }
    });

    copyBtns.forEach( (btns) => {
        btns.addEventListener('click', (e) => {
            alert('copied');
            navigator.clipboard.writeText(e.target.title);
        });
    });

    epic_gradient.forEach( (e) => {
        let listr = e.classList;
        for (let i = 0; i < listr.length; i++) {
            const element = listr[i];
            if (element == 'epic_gradient') {
                let no1 = i +=1;

                let col1 = listr[no1]
                apply_gradient(e, col1)
                break;
            }
        }
    });

    function apply_gradient(e, col) {
        e.style.backgroundImage = `linear-gradient${col}`
    }

    epic_bg.forEach( (e) => {
        let listr = e.classList;
        for (let i = 0; i < listr.length; i++) {
            const element = listr[i];
            if (element == 'epic_bg') {
                let no1 = i +=1;

                let col1 = listr[no1]
                apply_bg(e, col1)
                break;
            }
        }
    });

    function apply_bg(e, col1) {
        e.style.backgroundColor = `${col1}`
    }

    // Custom Functions
    function dropmenu(e) {
        qs('.epic_nav').classList.toggle('active')
        qs('.epic_nav').classList.toggle('up-in')
    }


    // Js inbuilt Functions
    observer = new IntersectionObserver(entries => {
        entries.forEach( entry => {
            if (entry.target.classList.contains('observe_once') && entry.isIntersecting) observer.unobserver(entry);
            if (entry.target.classList.contains('anim_left')) entry.target.classList.toggle("left-in", entry.isIntersecting);
            if (entry.target.classList.contains('anim_right')) entry.target.classList.toggle("right-in", entry.isIntersecting);
            if (entry.target.classList.contains('anim_up')) entry.target.classList.toggle("up-in", entry.isIntersecting);
            if (entry.target.classList.contains('anim_down')) entry.target.classList.toggle("down-in", entry.isIntersecting);
            if (entry.target.classList.contains('anim_roll')) entry.target.classList.toggle("roll-in", entry.isIntersecting);
            else entry.target.classList.toggle("right-in", entry.isIntersecting);
        }), 
        {
            rootMargin: "20px"
        }
    });

    observe_anim.forEach(card => {
        observer.observe(card);
    })
})


let links = [

    ['Packages/epic.css'],
    ['Packages/colour.css'],
    ['Packages/sizes.css'],
    ['Packages/style.css'],
    ['Packages/classes.css'],
    ['Packages/lg_classes.css'],
    ['Packages/md_classes.css'],
    ['Packages/sm_classes.css'],

    ['Packages/font.css'],
    ['Packages/icon.css'], 
    ['Packages/anim.css']

]

for (let i = 0; i < links.length; i++) {
    let linked = document.createElement('link');
    linked.type = 'text/css';
    linked.rel = 'stylesheet';
    linked.media = 'all'
    linked.href = `{% static "${links[i]}" %}`
    
    document.querySelector('head').append(linked);    
}