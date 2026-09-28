<template>

<div class="dashboard">


<h1>
Apply Leave
</h1>



<div class="card">


<label>
Reason
</label>

<br>

<textarea
v-model="form.reason"
placeholder="Enter leave reason"
></textarea>



<br><br>



<label>
Start Date
</label>

<br>

<input
type="date"
v-model="form.start_date"
/>



<br><br>



<label>
End Date
</label>

<br>

<input
type="date"
v-model="form.end_date"
/>



<br><br>



<button
@click="submitLeave"
>

Submit Leave

</button>



<p>
{{ message }}
</p>



</div>



</div>


</template>





<script>


import api from "../../api/axios";



export default {


data(){


return {


form:{


reason:"",

start_date:"",

end_date:""


},


message:""


}


},





methods:{



async submitLeave(){


try{


await api.post(

"/leaves/apply/",

this.form

);



this.message =
"Leave submitted successfully ✅";



this.form = {


reason:"",

start_date:"",

end_date:""


};



}


catch(error){

console.log(
"Leave Error:",
error.response?.data
);


this.message =
JSON.stringify(
error.response?.data
)
||
"Failed to submit leave ❌";


}

}



}



}






</script>