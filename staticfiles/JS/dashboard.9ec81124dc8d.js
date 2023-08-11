let shareBtn = document.querySelectorAll('.share-btn');
let draft = document.querySelector('#draft');
let settingBtn = document.querySelectorAll('.setting-btn');

shareBtn.forEach(r => r.addEventListener('click', shareLink));
settingBtn.forEach(r => r.addEventListener('click', toggleSettingRack));

function toggleSettingRack(e) {
    let setting_id = e.target.classList[1];
    let settingRacks = document.querySelectorAll('.setting-rack');

    for (let i = 0; i < settingRacks.length; i++) {
        const settingRack = settingRacks[i];
        if (settingRack.id == setting_id) {
            settingRack.classList.toggle('dp-none');
        } 
    }
}


function shareLink(li_nk) {

    if (navigator.share) {
        navigator.share({
            title: "Billmink App",
            text: "Could you help me with my bill?",
            url: li_nk
        });
    } else {
        window.location.href = `https://api.whatsapp.com/send?text=Could you help me with my bill? : ${li_nk}`;
    }
}

const formatter = Intl.NumberFormat(
    'en',
    {
        notation : "compact",
        style: 'currency',
        currency: 'NGN'
    }
)

function compac(params) {
    let n = params.title;
    params.innerText = formatter.format(n)
}

function toggleModal() {
    alert(' Something ')
}