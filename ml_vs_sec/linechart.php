 
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
          ['keyword', 'paper count'],
          <?php
		  
		  $query = "SELECT DISTINCT year, COUNT(year)  FROM `papers` GROUP BY year";
					
		  $result = mysqli_query($conn,$query);
		  if (mysqli_num_rows($result) > 0){
			  
			  while($row = mysqli_fetch_assoc($result)){
				  
				  echo "['".$row['year']."',".$row['COUNT(year)']."],";
				  
				  
			  }
			  
		  }else{
			  
			   echo "0 results";
			   echo "Error: " . $sql . "<br>" . mysqli_error($conn);
			  
		  }
		  
		  
		  ?>
        ]);

        var options = {
          title: 'Paper Count Based on Keyword',
          legend: { position: 'bottom' }
        };

        var chart = new google.visualization.LineChart(document.getElementById('linechart_material'));

        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id="linechart_material" style="width: 900px; height: 500px"></div>
  </body>
</html>


     