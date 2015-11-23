/**
 * Created by farabi on 11/15/15.
 */

function isEmpty(str){
    str = str.trim();
    return (!str || str.length==0);
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("SubmitButton").addEventListener('click',function ()
    {
        if(isEmpty(getElementById("status").innerHTML)){
            alert("This Should not be empty");
        }

    }  );
});