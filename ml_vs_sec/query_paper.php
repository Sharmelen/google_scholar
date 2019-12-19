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

echo "";



$year_range = mysqli_real_escape_string($conn,$_POST['year_range']);
$specific_year = mysqli_real_escape_string($conn,$_POST['specific_year']);
$cite_range = mysqli_real_escape_string($conn,$_POST['cite_range']);
//$author = mysqli_real_escape_string($conn,$_POST['author']);

//echo "You have selected :" .$year_range;

if($year_range == 1){ $sql = "SELECT * FROM paper WHERE year BETWEEN 1991 AND 1995"; $sql7 = "SELECT COUNT(title),year FROM paper WHERE year BETWEEN 1991 AND 1995 GROUP BY year"; }
elseif($year_range == 2){$sql = "SELECT * FROM paper WHERE year BETWEEN 1995 AND 1999";$sql7 = "SELECT COUNT(title),year FROM paper WHERE year BETWEEN 1995 AND 1999 GROUP BY year";}
elseif($year_range == 3){$sql = "SELECT * FROM paper WHERE year BETWEEN 1999 AND 2003";$sql7 = "SELECT COUNT(title),year FROM paper WHERE year BETWEEN 1999 AND 2003 GROUP BY year";}
elseif($year_range == 4){$sql = "SELECT * FROM paper WHERE year BETWEEN 2003 AND 2007";$sql7 = "SELECT COUNT(title),year FROM paper WHERE year BETWEEN 2003 AND 2007 GROUP BY year";}
elseif($year_range == 5){$sql = "SELECT * FROM paper WHERE year BETWEEN 2007 AND 2011";$sql7 = "SELECT COUNT(title),year FROM paper WHERE year BETWEEN 2007 AND 2011 GROUP BY year";}
elseif($year_range == 6){$sql = "SELECT * FROM paper WHERE year BETWEEN 2011 AND 2015";$sql7 = "SELECT COUNT(title),year FROM paper WHERE year BETWEEN 2011 AND 2015 GROUP BY year";}
elseif($year_range == 7){$sql = "SELECT * FROM paper WHERE year BETWEEN 2015 AND 2019";$sql7 = "SELECT COUNT(title),year FROM paper WHERE year BETWEEN 2015 AND 2019 GROUP BY year";}
elseif($year_range == 0){$sql = "SELECT * FROM paper WHERE year BETWEEN 0 AND 1;";}

$flag_year_range = FALSE;

if($year_range >= 1 && $cite_range == 0){
	
	$result = mysqli_query($conn,$sql);
	
	if (mysqli_num_rows($result) > 0) {
		// output data of each row
		$flag_year_range = TRUE;
		while($row = mysqli_fetch_assoc($result)) {
			echo "title: " . $row["title"]. " - year: " . $row["year"]. "<br>";
		}
	} 
	else {
		$flag_year_range = FALSE;
		echo "no year";
}


if($specific_year == 0){echo"";}
else{
	
	$sql2 = "SELECT * FROM paper WHERE year = '$specific_year';";
	$result2 = mysqli_query($conn,$sql2);
	
	if (mysqli_num_rows($result2) > 0) {
    // output data of each row
    while($row = mysqli_fetch_assoc($result2)) {
        echo "title: " . $row["title"]. " - year: " . $row["year"]. "<br>";
    }
} else {
    echo "Could not find paper published on year $specific_year";
}
} 
}


if($cite_range == 1){ $sql3 = "SELECT * FROM paper WHERE citation BETWEEN 0 AND 99"; $sql8 = "SELECT COUNT(title),year FROM paper WHERE citation BETWEEN 0 AND 99 GROUP BY year"; }
elseif($cite_range == 2){$sql3 = "SELECT * FROM paper WHERE citation BETWEEN 100 AND 499"; $sql8 = "SELECT COUNT(title),year FROM paper WHERE citation BETWEEN 100 AND 499 GROUP BY year";}
elseif($cite_range == 3){$sql3 = "SELECT * FROM paper WHERE citation BETWEEN 500 AND 999"; $sql8 = "SELECT COUNT(title),year FROM paper WHERE citation BETWEEN 500 AND 999 GROUP BY year";}
elseif($cite_range == 4){$sql3 = "SELECT * FROM paper WHERE citation BETWEEN 1000 AND 1499"; $sql8 = "SELECT COUNT(title),year FROM paper WHERE citation BETWEEN 1000 AND 1499 GROUP BY year";}
elseif($cite_range == 5){$sql3 = "SELECT * FROM paper WHERE citation >= 1500 "; $sql8 = "SELECT COUNT(title),year FROM paper WHERE citation >= GROUP BY year";}
elseif($cite_range == 0){$sql3 = "SELECT * FROM paper WHERE title = 'xxxx';";}

$flag_cite_range = FALSE;

if($cite_range >= 1 && $year_range == 0){
	
	$result3 = mysqli_query($conn,$sql3);
	
	if (mysqli_num_rows($result3) > 0) {
	// output data of each row
	$flag_cite_range = TRUE;
	$flag_year_range = FALSE;
	while($row = mysqli_fetch_assoc($result3)) {
		echo "title: " . $row["title"]. " - citation: " . $row["citation"]. "<br>";
	}
} else {
	//echo "Error: " . $sql . "<br>" . mysqli_error($conn);
	//echo "paper not found";
}
}
else{
	$flag_cite_range = FALSE;
}


$flag_cite_year_range = FALSE;
if($cite_range >=1 && $year_range >=1){
	
	$flag_cite_year_range = TRUE;
	$multiquery = " $sql UNION $sql3;";
	
	//echo"".$multiquery;
	$result11 = mysqli_query($conn,$multiquery);
	
	if (mysqli_num_rows($result11) > 0) {
	// output data of each row
	
	while($row = mysqli_fetch_assoc($result11)) {
		echo "title: " . $row["title"]. " - citation: " . $row["citation"]. "<br>";
	}
} else {
	//echo "Error: " . $sql . "<br>" . mysqli_error($conn);
	echo "paper not found";
}

	
}




?>

<?php if($flag_year_range == TRUE){ echo"ok"; ?>


 <html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['year', 'paper count'],
          <?php
		  
		  
		  	
		  $result4 = mysqli_query($conn,$sql7);
		  if (mysqli_num_rows($result4) > 0){
			  
			  while($row = mysqli_fetch_assoc($result4)){
				  
				  echo "['".$row['year']."',".$row['COUNT(title)']."],";
				  
				  
			  }
			  
		  }else{
			  
			   echo "0 results";
			   echo "Error: " . $sql . "<br>" . mysqli_error($conn);
			  
		  }
		  
		  
		  ?>
        ]);

        var options = {
          title: 'Paper Count Based on Year',
          legend: { position: 'bottom' }
        };

        var chart = new google.visualization.LineChart(document.getElementById('linechart_material'));

        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
  <h1>test</>
    <div id="linechart_material" style="width: 900px; height: 500px"></div>
  </body>
</html>

<?php } ?>






<?php if($flag_cite_range == TRUE ){ echo""; ?>


 <html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['year', 'paper count'],
          <?php
		  
		  
		  	
		  $result4 = mysqli_query($conn,$sql8);
		  if (mysqli_num_rows($result4) > 0){
			  
			  while($row = mysqli_fetch_assoc($result4)){
				  
				  echo "['".$row['year']."',".$row['COUNT(title)']."],";
				  
				  
			  }
			  
		  }else{
			  
			   echo "0 results";
			   echo "Error: " . $sql . "<br>" . mysqli_error($conn);
			  
		  }
		  
		  
		  ?>
        ]);

        var options = {
          title: 'Paper Count Based on Citation',
          legend: { position: 'bottom' }
        };

        var chart = new google.visualization.LineChart(document.getElementById('linechart_material'));

        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
  <h1>test</>
    <div id="linechart_material" style="width: 900px; height: 500px"></div>
  </body>
</html>

<?php } ?>



<?php if($flag_cite_year_range == TRUE ){ echo"hello"; ?>

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
		  
		  $query = "$sql7 UNION $sql8";
					
		  $result = mysqli_query($conn,$query);
		  if (mysqli_num_rows($result) > 0){
			  
			  while($row = mysqli_fetch_assoc($result)){
				  
				  echo "['".$row['year']."',".$row['COUNT(title)']."],";
				  
				  
			  }
			  
		  }else{
			  
			   echo "0 results";
			   echo "Error: " . $sql . "<br>" . mysqli_error($conn);
			  
		  }
		  
		  
		  ?>
        ]);

        var options = {
          title: 'Paper Count Based on Citation Number',
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


<?php } ?>


