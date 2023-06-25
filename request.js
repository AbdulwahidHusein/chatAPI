let header = {'method':'POST',
'headers':{'Content-Type':'application/json'},
'body':{'email':'abdi@gmail.com', 'password':'abdi'}}

const retrive = async ()=>{
    let response = await fetch('http://127.0.0.1:8000/api/token/', header)
    console.log(response)
}
retrive()