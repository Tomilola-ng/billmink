function shareLink(li_nk, msg = "Could you help me with my bill?") {

    if (navigator.share) {
        navigator.share({
            title: "Billmink App",
            text: msg,
            url: li_nk
        });
    } else {
        window.location.href = `https://api.whatsapp.com/send?text=${msg} : ${li_nk}`;
    }
}