function getRandomDates() {
    const now = new Date();
    const pastWeek = new Date(now.getTime() - 7 * 24 * 360000 );
    const randomTimestamp = pastWeek.getTime() + Math.random() * (now.getTime() - pastWeek.getTime());
    const randomDate = new Date(randomTimestamp);
    const month = randomDate.toLocaleString('default', { month: 'long'});
    const date = randomDate.getDate();
    const year = randomDate.getFullYear();

    return `${month} ${date}, ${year}`
}

function getRandomAmount() {
    let amount = Math.floor(Math.random() * 1000000) / 100;
    return amount;
}

function getRandomBill() {
    let bill_types = ['Service Bill', 'Product Bill', 'Rental fee', 'Hosting fee', 'Repair Bill', 'consultation' ];
    let randomBill = bill_types[Math.floor(Math.random() * bill_types.length)];
    return randomBill;
}

let svg = document.getElementById('page_svg');
let main_illustration = document.querySelector('.main_illustration');
let bill_value = document.querySelector('#bill_value');
let bill_date = document.querySelector('#bill_date');
let bill_type = document.querySelector('#bill_type');

function updateBill() {
    main_illustration.classList.add('left-in');
    bill_value.textContent = getRandomAmount()
    bill_date.textContent = getRandomDates()
    bill_type.textContent = getRandomBill()

    setTimeout(() => {
        main_illustration.classList.remove('left-in');                    
    }, 2000);
}

setInterval(updateBill, 5000);