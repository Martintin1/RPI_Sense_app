var XMLHttp = new XMLHttpRequest();

function startMeasure()
{
    if(XMLHttp.readyState == 0 || XMLHttp.readyState == 4)
    {
        XMLHttp.open("GET", "/ajax", true);
        XMLHttp.onreadystatechange = handleServerResponse; // anropas da man far ett svar
        XMLHttp.send(null);
        setTimeout('startMeasure()',1000);
    }
    else
    {
        //alert("korvTimeout")
        setTimeout('startMeasure()',1000); //vanta en sekund, sedan prova igen
    }
}

function handleServerResponse()
{
    if(XMLHttp.readyState == 4)
    {
        if(XMLHttp.status == 200) //om verforingen funkade
        {
        json = JSON.parse(XMLHttp.responseText);
        document.getElementById("tempDiv").innerHTML = 'Temp: ' + json.Temp;
        document.getElementById("pressureDiv").innerHTML = 'Tryck: ' + json.Pressure;
        }
        else
        {
            //alert("korv5")
        }
    }
}

function displayText()
{
    if(XMLHttp.readyState == 0 || XMLHttp.readyState == 4)
    {
        XMLHttp.open("GET", "/displaytext", true);
        XMLHttp.send(null);
    }
}