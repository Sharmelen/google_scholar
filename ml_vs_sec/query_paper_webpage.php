<?php

$servername = "37.59.55.185";
$username = "ZejMYc2nXj";
$password = "TtEI93o66O";
$dbname = "ZejMYc2nXj";

// Create connection
$conn = mysqli_connect($servername, $username, $password,$dbname);

// Check connection
if (!$conn) {
	
    die("Connection failed: " . mysqli_connect_error());
	
}
else{
	echo"";
}
?>
 
 
 
 
 <html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable([
        ["Year", "Paper Count", { role: "style" } ],
		
		  
		<?php
		  
			  $query = "SELECT DISTINCT year, COUNT(*) FROM `paper` GROUP BY year ORDER BY year";
						
			  $result = mysqli_query($conn,$query);
			  if (mysqli_num_rows($result) > 0){
				  
				  while($row = mysqli_fetch_assoc($result)){
					  
					  echo "['".$row['year']."',".$row['COUNT(*)'].",'gold'],";
					  
					  
				  }
				  
			  }else{
				  
				   echo "0 results";
				   echo "Error: " . $sql . "<br>" . mysqli_error($conn);
				  
			  }
			  
			  
			  ?>
	        
	      ]);
      var options = {
        title: "Paper Count Based On Year",
        width: 600,
        height: 500,
        bar: {groupWidth: "95%"},
        legend: { position: "none" }
      };
        var chart = new google.visualization.LineChart(document.getElementById('linechart_material'));

        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id="linechart_material" style="width: 900px; height: 500px"></div>
	<p>Number of papers collected: 
		<?php
		  
		  $query = "SELECT COUNT(*) FROM `paper`";
					
		  $result = mysqli_query($conn,$query);
		  if (mysqli_num_rows($result) > 0){
			  
			  while($row = mysqli_fetch_assoc($result)){
				  
				  echo $row['COUNT(*)'];
				  
			  }
			  
		  }else{
			  
			   echo "0 results";
			   echo "Error: " . $sql . "<br>" . mysqli_error($conn);
			  
		  }
		  
		  
		  ?>
    </p>
  </body>
</html>





<html>
<form action="query_paper.php" method = "POST">
Paper Query

<p>Select range of year in which paper is published</p>
	<input type="radio" name="year_range" value="0" checked>None<br>
	<input type="radio" name="year_range" value="1"> 1991 - 1995<br>
	<input type="radio" name="year_range" value="2"> 1995 - 1999<br>
	<input type="radio" name="year_range" value="3"> 1999 - 2003<br>
	<input type="radio" name="year_range" value="4"> 2003 - 2007<br>
	<input type="radio" name="year_range" value="5"> 2007 - 2011<br>
	<input type="radio" name="year_range" value="6"> 2011 - 2015<br>
	<input type="radio" name="year_range" value="7"> 2015 - 2019<br>


	
Select paper based on a specific year<br>

<input type="text" name="specific_year" value = "0"><br>

<p>Select paper based on a range of citation</p> 
	<input type="radio" name="cite_range" value="0" checked>None<br>
	<input type="radio" name="cite_range" value="1"> 0 - 99<br>
	<input type="radio" name="cite_range" value="2"> 100 - 499<br>
	<input type="radio" name="cite_range" value="3"> 500 - 999<br>
	<input type="radio" name="cite_range" value="4"> 1000 - 1499<br>
	<input type="radio" name="cite_range" value="5"> 1500 and above<br>

Select paper based on specific author name(note that the author must be a main author or co author of this paper)

<input type="text" name="author" value = "John Doe"><br>

<input type = 'submit' value = 'submit'>

</form>



</html>