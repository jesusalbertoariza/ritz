function obtenerFecha(){
    let today = new Date();
    let day = today.getFullYear() + '-' + (today.getMonth()+1) + '-' + today.getDate();
    return day
}

let dia = obtenerFecha()

let checkin = document.querySelector('#check_in') //setAttribute('value','2022-10-12')
checkin.setAttribute('value',dia)
checkin.setAttribute('min',dia)

let checkout = document.querySelector('#check_out')
checkout.setAttribute('value',dia)
checkout.setAttribute('min',dia)