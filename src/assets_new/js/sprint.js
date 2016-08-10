 $(document).ready(function(){
/************************************************************add sprint page starts*****************************************************/
	 
/*************************************************************table sorting starts***************************************/

	 
/***********************************user story asce starts***************************************/
	 $(document).on('click',"#user_story_asce",function(){
		 //   alert('User Story Ascending');
		    
		    var s= window.location.href.split(".com/").pop();
		    var task_count=$('#task_count').val();
			 var userstory_asc='asce';
			 
		        if (s.indexOf("?sprint_key")>1)
		        {
		        	
		        	var sprintkey = GetParameterValues('sprint_key');
		        	
		        	//console.log(GetParameterValues('sprint_key'));
		        	
		        	var count = 0;
		        	if(GetParameterValues('count'))
		        	{
		        		count=GetParameterValues('count')
		        	}
		        	else	
		        	{
		        		if(task_count != 15)
		        			{
		        			count = task_count;
		        			}
		        		
		        	}
		        		
		        	
		        	if(count)
		        	{
		        			$.get( '/sprint?sprint_key='+sprintkey+'&count='+count+'&userstory='+userstory_asc ,function( data ) {
		        		
		        				//console.log(data);
		        				
		        			$('#tasks_sprints').load( '/sprint?sprint_key='+sprintkey+'&count='+count+'&userstory='+userstory_asc+' #tasks_sprints', function(result) {
				  			
			  				
			  				$(".table").each(function(){
								if (!$(this).find("tr.find_empty").length){
								a=$(this).find("tbody")[0];
								$(a).append("<tr><td colspan='10' align='center'>There are no tasks in the sprint</td></tr>")
								}
								
							})
							
							$("#task_count option[value=" + count+"]").prop("selected","selected") ;
							
		        			});	
		    			
		    		
		    			
		    			
		        			});
		        	}
		        	
		        	else
		        		{
		        		
		        				$.get( '/sprint?sprint_key='+sprintkey+'&userstory='+userstory_asc ,function( data ) {
			        		
		        					//console.log(data);
		        					
		        				$('#tasks_sprints').load( '/sprint?sprint_key='+sprintkey+'&userstory='+userstory_asc+' #tasks_sprints', function(result) {
						  			
					  				
					  			$(".table").each(function(){
										if (!$(this).find("tr.find_empty").length){
										a=$(this).find("tbody")[0];
										$(a).append("<tr><td colspan='10' align='center'>There are no tasks in the sprint</td></tr>")
										}
										
									})
									
									$("#task_count option[value=" + count+"]").prop("selected","selected") ;
									
					  			});	
				    			
				    		
				    			
				    			
		        				});
		        		}
		        	
		        }
		        else
		        {
		        	
		        		$.get( '/sprint?userstory='+userstory_asc ,function( data ) {
		        		
		        			//console.log(data);
		        			
		        			$('#tasks_sprints').load('/sprint?userstory='+userstory_asc+' #tasks_sprints', function(result) {
					  			
				  				
				  				$(".table").each(function(){
									if (!$(this).find("tr.find_empty").length){
									a=$(this).find("tbody")[0];
									$(a).append("<tr><td colspan='10' align='center'>There are no tasks in the sprint</td></tr>")
									}
									
								})
								
								$("#task_count option[value=" + count+"]").prop("selected","selected") ;
								
				  			});	
		        	
		    		});
		        }
		    
		    
		    
		});
	 
/***********************************user story asce ends***************************************/
	 
/***********************************user story desc starts***************************************/
	 
	 $(document).on('click',"#user_story_desc",function(){
		  //  alert('User Story Desending');
		    
		    var s= window.location.href.split(".com/").pop();
		    var task_count=$('#task_count').val();
			 var userstory_desc='desc';
			 
		        if (s.indexOf("?sprint_key")>1)
		        {
		        	
		        	var sprintkey = GetParameterValues('sprint_key');
		        	
		        	//console.log(GetParameterValues('sprint_key'));
		        	
		        	var count = 0;
		        	if(GetParameterValues('count'))
		        	{
		        		count=GetParameterValues('count')
		        	}
		        	else	
		        	{
		        		if(task_count != 15)
		        			{
		        			count = task_count;
		        			}
		        		
		        	}
		        	
		        	if(count)
		        	{
		        			$.get( '/sprint?sprint_key='+sprintkey+'&count='+count+'&userstory='+userstory_desc ,function( data ) {
		        		
		        			//	console.log(data);
		        				
		        			$('#tasks_sprints').load( '/sprint?sprint_key='+sprintkey+'&count='+count+'&userstory='+userstory_desc+' #tasks_sprints', function(result) {
				  			
			  				
			  				$(".table").each(function(){
								if (!$(this).find("tr.find_empty").length){
								a=$(this).find("tbody")[0];
								$(a).append("<tr><td colspan='10' align='center'>There are no tasks in the sprint</td></tr>")
								}
								
							})
							
							$("#task_count option[value=" + count+"]").prop("selected","selected") ;
							
		        			});	
		    			
		    		
		    			
		    			
		        			});
		        	}
		        	
		        	else
		        		{
		        		
		        				$.get( '/sprint?sprint_key='+sprintkey+'&userstory='+userstory_desc ,function( data ) {
			        		
		        				//	console.log(data);
		        					
		        				$('#tasks_sprints').load( '/sprint?sprint_key='+sprintkey+'&userstory='+userstory_desc+' #tasks_sprints', function(result) {
						  			
					  				
					  			$(".table").each(function(){
										if (!$(this).find("tr.find_empty").length){
										a=$(this).find("tbody")[0];
										$(a).append("<tr><td colspan='10' align='center'>There are no tasks in the sprint</td></tr>")
										}
										
									})
									
									$("#task_count option[value=" + count+"]").prop("selected","selected") ;
									
					  			});	
				    			
				    		
				    			
				    			
		        				});
		        		}
		        	
		        }
		        else
		        {
		        	
		        		$.get( '/sprint?userstory='+userstory_asc ,function( data ) {
		        		
		        		//	console.log(data);
		        			
		        			$('#tasks_sprints').load('/sprint?userstory='+userstory_desc+' #tasks_sprints', function(result) {
					  			
				  				
				  				$(".table").each(function(){
									if (!$(this).find("tr.find_empty").length){
									a=$(this).find("tbody")[0];
									$(a).append("<tr><td colspan='10' align='center'>There are no tasks in the sprint</td></tr>")
									}
									
								})
								
								$("#task_count option[value=" +count+"]").prop("selected","selected") ;
								
				  			});	
		        	
		    		});
		        }
		    
		    
		    
		});	 
	 
/***********************************user story desc ends***************************************/
	 
/***********************************planned start date asce starts*******************************/
	 $(document).on('click',"#planned_startdate_asce",function(){
		  //  alert('Planned start date Ascending');
		    
		    
		    var s= window.location.href.split(".com/").pop();
		    var task_count=$('#task_count').val();
			 var planned_startdate='asce';
			 
		        if (s.indexOf("?sprint_key")>1)
		        {
		        	
		        	var sprintkey = GetParameterValues('sprint_key');
		        	
		        //	console.log(GetParameterValues('sprint_key'));
		        	
		        	var count = 0;
		        	if(GetParameterValues('count'))
		        	{
		        		count=GetParameterValues('count')
		        	}
		        	else	
		        	{
		        		if(task_count != 15)
		        			{
		        			count = task_count;
		        			}
		        		
		        	}
		        	
		        	if(count)
		        	{
		        			$.get( '/sprint?sprint_key='+sprintkey+'&count='+count+'&planned_startdate='+planned_startdate ,function( data ) {
		        		
		        			//	console.log(data);
		        				
		        			$('#tasks_sprints').load( '/sprint?sprint_key='+sprintkey+'&count='+count+'&planned_startdate='+planned_startdate+' #tasks_sprints', function(result) {
				  			
			  				
			  				$(".table").each(function(){
								if (!$(this).find("tr.find_empty").length){
								a=$(this).find("tbody")[0];
								$(a).append("<tr><td colspan='10' align='center'>There are no tasks in the sprint</td></tr>")
								}
								
							})
							
							$("#task_count option[value=" + count+"]").prop("selected","selected") ;
							
		        			});	
		    			
		    		
		    			
		    			
		        			});
		        	}
		        	
		        	else
		        		{
		        		
		        				$.get( '/sprint?sprint_key='+sprintkey+'&planned_startdate='+planned_startdate ,function( data ) {
			        		
		        				//	console.log(data);
		        					
		        				$('#tasks_sprints').load( '/sprint?sprint_key='+sprintkey+'&planned_startdate='+planned_startdate+' #tasks_sprints', function(result) {
						  			
					  				
					  			$(".table").each(function(){
										if (!$(this).find("tr.find_empty").length){
										a=$(this).find("tbody")[0];
										$(a).append("<tr><td colspan='10' align='center'>There are no tasks in the sprint</td></tr>")
										}
										
									})
									
									$("#task_count option[value=" + count+"]").prop("selected","selected") ;
									
					  			});	
				    			
				    		
				    			
				    			
		        				});
		        		}
		        	
		        }
		        else
		        {
		        	
		        		$.get( '/sprint?planned_startdate='+planned_startdate ,function( data ) {
		        		
		        		//	console.log(data);
		        			
		        			$('#tasks_sprints').load('/sprint?planned_startdate='+planned_startdate+' #tasks_sprints', function(result) {
					  			
				  				
				  				$(".table").each(function(){
									if (!$(this).find("tr.find_empty").length){
									a=$(this).find("tbody")[0];
									$(a).append("<tr><td colspan='10' align='center'>There are no tasks in the sprint</td></tr>")
									}
									
								})
								
								$("#task_count option[value=" + count+"]").prop("selected","selected") ;
								
				  			});	
		        	
		    		});
		        }
		    
		    
		    
		});	 
	 
/***********************************planned start date asce ends*******************************/

/***********************************planned start date desc starts*******************************/
	 $(document).on('click',"#planned_startdate_desc",function(){
		  //  alert('Planned start date Desending');
		    
		    

		    var s= window.location.href.split(".com/").pop();
		    var task_count=$('#task_count').val();
			 var planned_startdate='desc';
			 
		        if (s.indexOf("?sprint_key")>1)
		        {
		        	
		        	var sprintkey = GetParameterValues('sprint_key');
		        	
		        //	console.log(GetParameterValues('sprint_key'));
		        	
		        	var count = 0;
		        	if(GetParameterValues('count'))
		        	{
		        		count=GetParameterValues('count')
		        	}
		        	else	
		        	{
		        		if(task_count != 15)
		        			{
		        			count = task_count;
		        			}
		        		
		        	}
		        	
		        	if(count)
		        	{
		        			$.get( '/sprint?sprint_key='+sprintkey+'&count='+count+'&planned_startdate='+planned_startdate ,function( data ) {
		        		
		        			//	console.log(data);
		        				
		        			$('#tasks_sprints').load( '/sprint?sprint_key='+sprintkey+'&count='+count+'&planned_startdate='+planned_startdate+' #tasks_sprints', function(result) {
				  			
			  				
			  				$(".table").each(function(){
								if (!$(this).find("tr.find_empty").length){
								a=$(this).find("tbody")[0];
								$(a).append("<tr><td colspan='10' align='center'>There are no tasks in the sprint</td></tr>")
								}
								
							})
							
							$("#task_count option[value=" + count+"]").prop("selected","selected") ;
							
		        			});	
		    			
		    		
		    			
		    			
		        			});
		        	}
		        	
		        	else
		        		{
		        		
		        				$.get( '/sprint?sprint_key='+sprintkey+'&planned_startdate='+planned_startdate ,function( data ) {
			        		
		        					//console.log(data);
		        					
		        				$('#tasks_sprints').load( '/sprint?sprint_key='+sprintkey+'&planned_startdate='+planned_startdate+' #tasks_sprints', function(result) {
						  			
					  				
					  			$(".table").each(function(){
										if (!$(this).find("tr.find_empty").length){
										a=$(this).find("tbody")[0];
										$(a).append("<tr><td colspan='10' align='center'>There are no tasks in the sprint</td></tr>")
										}
										
									})
									
									$("#task_count option[value=" + count+"]").prop("selected","selected") ;
									
					  			});	
				    			
				    		
				    			
				    			
		        				});
		        		}
		        	
		        }
		        else
		        {
		        	
		        		$.get( '/sprint?planned_startdate='+planned_startdate ,function( data ) {
		        		
		        			//console.log(data);
		        			
		        			$('#tasks_sprints').load('/sprint?planned_startdate='+planned_startdate+' #tasks_sprints', function(result) {
					  			
				  				
				  				$(".table").each(function(){
									if (!$(this).find("tr.find_empty").length){
									a=$(this).find("tbody")[0];
									$(a).append("<tr><td colspan='10' align='center'>There are no tasks in the sprint</td></tr>")
									}
									
								})
								
								$("#task_count option[value=" + count+"]").prop("selected","selected") ;
								
				  			});	
		        	
		    		});
		        }
		    
		    
		});	 
	 
/***********************************planned start date desc ends*******************************/

/***********************************planned end date asce starts*******************************/
	 
	 $(document).on('click',"#planned_enddate_asce",function(){
		 //   alert('Planned end date Ascending');
		    

		    var s= window.location.href.split(".com/").pop();
		    var task_count=$('#task_count').val();
			 var planned_enddate='asce';
			 
		        if (s.indexOf("?sprint_key")>1)
		        {
		        	
		        	var sprintkey = GetParameterValues('sprint_key');
		        	
		     //   	console.log(GetParameterValues('sprint_key'));
		        	
		        	var count = 0;
		        	if(GetParameterValues('count'))
		        	{
		        		count=GetParameterValues('count')
		        	}
		        	else	
		        	{
		        		if(task_count != 15)
		        			{
		        			count = task_count;
		        			}
		        		
		        	}
		        	
		        	if(count)
		        	{
		        			$.get( '/sprint?sprint_key='+sprintkey+'&count='+count+'&planned_enddate='+planned_enddate ,function( data ) {
		        		
		        			//	console.log(data);
		        				
		        			$('#tasks_sprints').load( '/sprint?sprint_key='+sprintkey+'&count='+count+'&planned_enddate='+planned_enddate+' #tasks_sprints', function(result) {
				  			
			  				
			  				$(".table").each(function(){
								if (!$(this).find("tr.find_empty").length){
								a=$(this).find("tbody")[0];
								$(a).append("<tr><td colspan='10' align='center'>There are no tasks in the sprint</td></tr>")
								}
								
							})
							
							$("#task_count option[value=" + count+"]").prop("selected","selected") ;
							
		        			});	
		    			
		    		
		    			
		    			
		        			});
		        	}
		        	
		        	else
		        		{
		        		
		        				$.get( '/sprint?sprint_key='+sprintkey+'&planned_enddate='+planned_enddate ,function( data ) {
			        		
		        				//	console.log(data);
		        					
		        				$('#tasks_sprints').load( '/sprint?sprint_key='+sprintkey+'&planned_enddate='+planned_enddate+' #tasks_sprints', function(result) {
						  			
					  				
					  			$(".table").each(function(){
										if (!$(this).find("tr.find_empty").length){
										a=$(this).find("tbody")[0];
										$(a).append("<tr><td colspan='10' align='center'>There are no tasks in the sprint</td></tr>")
										}
										
									})
									
									$("#task_count option[value=" + count+"]").prop("selected","selected") ;
									
					  			});	
				    			
				    		
				    			
				    			
		        				});
		        		}
		        	
		        }
		        else
		        {
		        	
		        		$.get( '/sprint?planned_enddate='+planned_enddate ,function( data ) {
		        		
		        		//	console.log(data);
		        			
		        			$('#tasks_sprints').load('/sprint?planned_enddate='+planned_enddate+' #tasks_sprints', function(result) {
					  			
				  				
				  				$(".table").each(function(){
									if (!$(this).find("tr.find_empty").length){
									a=$(this).find("tbody")[0];
									$(a).append("<tr><td colspan='10' align='center'>There are no tasks in the sprint</td></tr>")
									}
									
								})
								
								$("#task_count option[value=" + count+"]").prop("selected","selected") ;
								
				  			});	
		        	
		    		});
		        }
		    
		    
		});	 
	 
/***********************************planned end date asce ends*******************************/
	
/***********************************planned start date desc starts*******************************/
	 $(document).on('click',"#planned_enddate_desc",function(){
		    //alert('Planned end date Desending');
		    

		    var s= window.location.href.split(".com/").pop();
		    var task_count=$('#task_count').val();
			 var planned_enddate='desc';
			 
		        if (s.indexOf("?sprint_key")>1)
		        {
		        	
		        	var sprintkey = GetParameterValues('sprint_key');
		        	
		        //	console.log(GetParameterValues('sprint_key'));
		        	
		        	var count = 0;
		        	if(GetParameterValues('count'))
		        	{
		        		count=GetParameterValues('count')
		        	}
		        	else	
		        	{
		        		if(task_count != 15)
		        			{
		        			count = task_count;
		        			}
		        		
		        	}
		        	
		        	if(count)
		        	{
		        			$.get( '/sprint?sprint_key='+sprintkey+'&count='+count+'&planned_enddate='+planned_enddate ,function( data ) {
		        		
		        			$('#tasks_sprints').load( '/sprint?sprint_key='+sprintkey+'&count='+count+'&planned_enddate='+planned_enddate+' #tasks_sprints', function(result) {
				  			
			  				
			  				$(".table").each(function(){
								if (!$(this).find("tr.find_empty").length){
								a=$(this).find("tbody")[0];
								$(a).append("<tr><td colspan='10' align='center'>There are no tasks in the sprint</td></tr>")
								}
								
							})
							
							$("#task_count option[value=" + count+"]").prop("selected","selected") ;
							
		        			});	
		    			
		    		
		    			
		    			
		        			});
		        	}
		        	
		        	else
		        		{
		        		
		        				$.get( '/sprint?sprint_key='+sprintkey+'&planned_enddate='+planned_enddate ,function( data ) {
			        		
		        				$('#tasks_sprints').load( '/sprint?sprint_key='+sprintkey+'&planned_enddate='+planned_enddate+' #tasks_sprints', function(result) {
						  			
					  				
					  			$(".table").each(function(){
										if (!$(this).find("tr.find_empty").length){
										a=$(this).find("tbody")[0];
										$(a).append("<tr><td colspan='10' align='center'>There are no tasks in the sprint</td></tr>")
										}
										
									})
									
									$("#task_count option[value=" + count+"]").prop("selected","selected") ;
									
					  			});	
				    			
				    		
				    			
				    			
		        				});
		        		}
		        	
		        }
		        else
		        {
		        	
		        		$.get( '/sprint?planned_enddate='+planned_enddate ,function( data ) {
		        		
		        			$('#tasks_sprints').load('/sprint?planned_enddate='+planned_enddate+' #tasks_sprints', function(result) {
					  			
				  				
				  				$(".table").each(function(){
									if (!$(this).find("tr.find_empty").length){
									a=$(this).find("tbody")[0];
									$(a).append("<tr><td colspan='10' align='center'>There are no tasks in the sprint</td></tr>")
									}
									
								})
								
								$("#task_count option[value=" + count+"]").prop("selected","selected") ;
								
				  			});	
		        	
		    		});
		        }
		    
		    
		});	 
	 
/***********************************planned start date desc ends*******************************/

/***********************************effort estimation asce starts*******************************/
	 $(document).on('click',"#estimation_effort_asce",function(){
		    //alert('Effort estimation Ascending');
		    

		    var s= window.location.href.split(".com/").pop();
		    var task_count=$('#task_count').val();
			 var efforts='asce';
			 
		        if (s.indexOf("?sprint_key")>1)
		        {
		        	
		        	var sprintkey = GetParameterValues('sprint_key');
		        	
		        	//console.log(GetParameterValues('sprint_key'));
		        	
		        	var count = 0;
		        	if(GetParameterValues('count'))
		        	{
		        		count=GetParameterValues('count')
		        	}
		        	else	
		        	{
		        		if(task_count != 15)
		        			{
		        			count = task_count;
		        			}
		        		
		        	}
		        	
		        	if(count)
		        	{
		        			$.get( '/sprint?sprint_key='+sprintkey+'&count='+count+'&efforts='+efforts ,function( data ) {
		        		
		        			$('#tasks_sprints').load( '/sprint?sprint_key='+sprintkey+'&count='+count+'&efforts='+efforts+' #tasks_sprints', function(result) {
				  			
			  				
			  				$(".table").each(function(){
								if (!$(this).find("tr.find_empty").length){
								a=$(this).find("tbody")[0];
								$(a).append("<tr><td colspan='10' align='center'>There are no tasks in the sprint</td></tr>")
								}
								
							})
							
							$("#task_count option[value=" + count+"]").prop("selected","selected") ;
							
		        			});	
		    			
		    		
		    			
		    			
		        			});
		        	}
		        	
		        	else
		        		{
		        		
		        				$.get( '/sprint?sprint_key='+sprintkey+'&efforts='+efforts ,function( data ) {
			        		
		        				$('#tasks_sprints').load( '/sprint?sprint_key='+sprintkey+'&efforts='+efforts+' #tasks_sprints', function(result) {
						  			
					  				
					  			$(".table").each(function(){
										if (!$(this).find("tr.find_empty").length){
										a=$(this).find("tbody")[0];
										$(a).append("<tr><td colspan='10' align='center'>There are no tasks in the sprint</td></tr>")
										}
										
									})
									
									$("#task_count option[value=" + count+"]").prop("selected","selected") ;
									
					  			});	
				    			
				    		
				    			
				    			
		        				});
		        		}
		        	
		        }
		        else
		        {
		        	
		        		$.get( '/sprint?planned_enddate='+planned_enddate ,function( data ) {
		        		
		        			$('#tasks_sprints').load('/sprint?efforts='+efforts+' #tasks_sprints', function(result) {
					  			
				  				
				  				$(".table").each(function(){
									if (!$(this).find("tr.find_empty").length){
									a=$(this).find("tbody")[0];
									$(a).append("<tr><td colspan='10' align='center'>There are no tasks in the sprint</td></tr>")
									}
									
								})
								
								$("#task_count option[value=" + count+"]").prop("selected","selected") ;
								
				  			});	
		        	
		    		});
		        }
		    
		    
		});	 
	 
/***********************************effort estimation asce ends*******************************/

/***********************************effort estimation desc starts*******************************/
	 $(document).on('click',"#estimation_effort_desc",function(){
		  //  alert('Effort estimation Desending');
		    
		    

		    var s= window.location.href.split(".com/").pop();
		    var task_count=$('#task_count').val();
			 var efforts='desc';
			 
		        if (s.indexOf("?sprint_key")>1)
		        {
		        	
		        	var sprintkey = GetParameterValues('sprint_key');
		        	
		        //	console.log(GetParameterValues('sprint_key'));
		        	
		        	var count = 0;
		        	if(GetParameterValues('count'))
		        	{
		        		count=GetParameterValues('count')
		        	}
		        	else	
		        	{
		        		if(task_count != 15)
		        			{
		        			count = task_count;
		        			}
		        		
		        	}
		        	
		        	if(count)
		        	{
		        			$.get( '/sprint?sprint_key='+sprintkey+'&count='+count+'&efforts='+efforts ,function( data ) {
		        		
		        			$('#tasks_sprints').load( '/sprint?sprint_key='+sprintkey+'&count='+count+'&efforts='+efforts+' #tasks_sprints', function(result) {
				  			
			  				
			  				$(".table").each(function(){
								if (!$(this).find("tr.find_empty").length){
								a=$(this).find("tbody")[0];
								$(a).append("<tr><td colspan='10' align='center'>There are no tasks in the sprint</td></tr>")
								}
								
							})
							
							$("#task_count option[value=" + count+"]").prop("selected","selected") ;
							
		        			});	
		    			
		    		
		    			
		    			
		        			});
		        	}
		        	
		        	else
		        		{
		        		
		        				$.get( '/sprint?sprint_key='+sprintkey+'&efforts='+efforts ,function( data ) {
			        		
		        				$('#tasks_sprints').load( '/sprint?sprint_key='+sprintkey+'&efforts='+efforts+' #tasks_sprints', function(result) {
						  			
					  				
					  			$(".table").each(function(){
										if (!$(this).find("tr.find_empty").length){
										a=$(this).find("tbody")[0];
										$(a).append("<tr><td colspan='10' align='center'>There are no tasks in the sprint</td></tr>")
										}
										
									})
									
									$("#task_count option[value=" + count+"]").prop("selected","selected") ;
									
					  			});	
				    			
				    		
				    			
				    			
		        				});
		        		}
		        	
		        }
		        else
		        {
		        	
		        		$.get( '/sprint?planned_enddate='+planned_enddate ,function( data ) {
		        		
		        			$('#tasks_sprints').load('/sprint?efforts='+efforts+' #tasks_sprints', function(result) {
					  			
				  				
				  				$(".table").each(function(){
									if (!$(this).find("tr.find_empty").length){
									a=$(this).find("tbody")[0];
									$(a).append("<tr><td colspan='10' align='center'>There are no tasks in the sprint</td></tr>")
									}
									
								})
								
								$("#task_count option[value=" + count+"]").prop("selected","selected") ;
								
				  			});	
		        	
		    		});
		        }
		    
		    
		    
		    
		});	 
	 
/***********************************effort estimation desc ends*******************************/	 
/*************************************************************table sorting ends***************************************/	
	 
/**************************************to get the query string starts*****************************************************/	 
		 function GetParameterValues(param) {
		 var url = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
		 for (var i = 0; i < url.length; i++) {
		 var urlparam = url[i].split('=');
		 if (urlparam[0] == param) {
		 return urlparam[1];
		 }
		 }
		 }
		 
/**************************************to get the query string ends*****************************************************/	

/**************************************to display count starts*****************************************************/	
		var count = GetParameterValues('count');
		if(count)
		{
				$("#task_count option[value=" + count+"]").prop("selected","selected") ;
		}
	 
/**************************************to display count ends*****************************************************/	
/*********************************************task count starts******************************************************/
	 $(document).on("change","#task_count",function() {
		 var s= window.location.href.split(".com/").pop();
		 var task_count=this.value;
	        if (s.indexOf("?sprint_key")>1)
	        {
	        	
	        	var sprintkey = GetParameterValues('sprint_key');
	        	
	        //	console.log(GetParameterValues('sprint_key'));
	        	
	        	
	        	$.get( '/sprint?sprint_key='+sprintkey+'&count='+task_count ,function( data ) {
	        		
	    		$('#tasks_sprints').load( '/sprint?sprint_key='+sprintkey+'&count='+task_count+' #tasks_sprints', function(result) {
			  			
		  				
		  				$(".table").each(function(){
							if (!$(this).find("tr.find_empty").length){
							a=$(this).find("tbody")[0];
							$(a).append("<tr><td colspan='10' align='center'>There are no tasks in the sprint</td></tr>")
							}
							
						})
						
						$("#task_count option[value=" + task_count+"]").prop("selected","selected") ;
						
		  			});	
	    			
	    		
	    			
	    			
	    		});
	        	
	        }
	        else
	        {
	        	
	        		$.get( '/sprint?count='+task_count ,function( data ) {
	        		
	    			//console.log(data);
	        		//	$('#task_table').html(data);
	    			
	        			$('#tasks_sprints').load('/sprint?count='+task_count+' #tasks_sprints', function(result) {
				  			
			  				
			  				$(".table").each(function(){
								if (!$(this).find("tr.find_empty").length){
								a=$(this).find("tbody")[0];
								$(a).append("<tr><td colspan='10' align='center'>There are no tasks in the sprint</td></tr>")
								}
								
							})
							
							$("#task_count option[value=" + task_count+"]").prop("selected","selected") ;
							
			  			});	
	        			
	    		//	window.location.href = '/sprint?count='+task_count;	
	    			
	    			
	    		//	$("#task_count").val(task_count).change();
	    			
	    		});
	        }
		 
	 });
	 
	 
/*********************************************task count ends********************************************************/
	 
/**************************************select sprint from dropdown start*********************************************/
	
	//alert($('#sprintselect').val());

 	$(document).on("change","#sprintselect",function() {
		
		var sprint_key =this.value;
		$.get( "/sprint?sprint_key="+sprint_key ,function( data ) {
		
			//console.log(data);
			
			window.location.href = "/sprint?sprint_key="+sprint_key;
  			
		});
	}); 
	

/**************************************select sprint from dropdown end*********************************************/
				
/******************************get release data starts**********************************************/					
				var releasel;
				release=$('#release').val();
				 var release_start_date;
				 var release_end_date;
					 
					if (release != 'None')
					{
						release=$('#release').val(); 
						$.post( "/release_info?key="+release+"")
				  		.done(function( data ) {
				  		
							//console.log(data);
						
							
							release_end_date= data;
						
				  		});
					}
						
/******************************get release data ends**********************************************/						

/******************************icon click starts**********************************************/	
					
					$('.form-group').find('.open-datetimepicker').on('click', function(){
					    $('#sprint_start').trigger('focus');
					});
					
					$('.form-group').find('.open-datetimepicker1').on('click', function(){
					    $('#sprint_end').trigger('focus');
					});
					
/******************************icon click ends**********************************************/						
					
/***********************sprint validation starts******************************/
					
					var sprint_validator=   $("#add_sprint").validate({
						      rules: {
						    	  name: 
						    	  {
						           		 required: true
						          },
						          start: 
						    	  {
						           		 required: true
						          },
						          end: 
						    	  {
						           		 required: true
						          },
						          desc: 
						          {
							      		 required: true
							      },
								  workinghours: 
								  {
										 required: true
										
									
								  }
						         },
						         messages: 
						         {
						        	 name: 
						           {
						             required: "Please enter sprint name."
						           },
						           start: 
							    	{
							           		 required: "Please enter start date."
							        },
							        end: 
							    	{
							           		 required: "Please enter end date."
							       },
						           desc: 
						           {
						             required: "Please enter sprint description."
						           },
						     
							       workinghours: 
							       {
							             required: "Please enter working hours."
							       }
							   
						         }
						     });
/****************************************sprint validation ends**************************************************/


/*****************************************to get release data on select starts*********************************/
					
					$('select').on('change', function (e) {
		
						release=$('#release').val(); 
						$.post( "/release_info?key="+release+"")
				  		.done(function( data ) {
				  			//alert(data);
							//console.log(data);
							release_end_date= data;
							
				  		});
	
	
					});
					
/*****************************************to get release data on select ends*********************************/	

/*****************************************for blank table rows starts****************************************/	
					$(".table").each(function(){
						if (!$(this).find("tr.find_empty").length){
						a=$(this).find("tbody")[0];
						$(a).append("<tr><td colspan='10' align='center'>There are no tasks in the sprint</td></tr>")
						}
						
					})
					if (!$('#empty_sprint').find("tr.find_empty").length){
						$('#empty_sprint').remove();
						
					}
					$('#tasks_sprints').on('load',function(){
						$(".table").each(function(){
												if (!$(this).find("tr.find_empty").length){
												a=$(this).find("tbody")[0];
												$(a).append("<tr><td colspan='10' align='center'>There are no tasks in the sprint</td></tr>")
												}
												
											})
											if (!$('#empty_sprint').find("tr.find_empty").length){
												$('#empty_sprint').remove();
												
											}
						})
						
/*****************************************for blank table rows ends****************************************/
					$(".nav-tabs a").click(function(){
						$(this).tab('show');
					});

/*****************************************datepicker starts***********************************************/
					$('body').on('focus',"#start,#start_edit", function(){
					    $(this).datepicker({
							format: 'dd/mm/yyyy',
							//startDate: '0d'
						});
					});
					$('body').on('focus',"#end,#end_edit", function(){
					    $(this).datepicker({
							format: 'dd/mm/yyyy',
							//startDate: '0d'
						});
					});
					$('.datepicker').datepicker({
						format: 'mm/dd/yyyy',
						//startDate: '0d',
						autoclose:true
					});
					$('.datepicker').datepicker()
				    .on('changeDate', function(e) {
				        $('.datepicker').datepicker('hide');
				    });
					
					
					$('#sprint_end').datepicker()
				    .on('changeDate', function(e) {
				    	if ($('#sprint_start').val()!=""){
					        start=$('#sprint_start').val();
					        end=$('#sprint_end').val();
					        secs=(new Date(end)).getTime()/1000-(new Date(start)).getTime()/1000
					        secs=secs/60/60/24;
					        if (secs>=7){
					        	week=parseInt(secs/7);
					        	days=secs%6;
					        	$("#length").val(week+" weeks "+days+" days")
					        }
					        else {
					        	if(secs==0){
					        		$("#length").val("1 Day")
					        	} else {
					        		secs=secs+1;
					        	$("#length").val(secs+" Days")
					        	}
					        }
				    	}
				    });
					$('#sprint_start').datepicker()
				    .on('changeDate', function(e) {
				    	if ($('#sprint_end').val()!=""){
				    		start=$('#sprint_start').val();
					        end=$('#sprint_end').val();
					        secs=(new Date(end)).getTime()/1000-(new Date(start)).getTime()/1000
					        secs=secs/60/60/24;
					        if (secs>=7){
					        	week=parseInt(secs/7);
					        	days=secs%6;
					        	$("#length").val(week+" weeks "+days+" days")
					        }
					        else {
					        	if(secs==0){
					        		$("#length").val("1 Day")
					        	} else {
					        		secs=secs+1;
					        	$("#length").val(secs+" Days")
					        	}
					        }
				    	}
				    });
					
					
/*****************************************datepicker ends***********************************************/
					/*$("#add-issue").click(function(e) {
						$('#add-issue-modal').modal('show');
					});*/
					
					
/*****************************************add sprint modal starts***********************************************/
					$("#add-sprint").click(function(e) {
						$('#add-sprint-modal').modal('show');
					});

					
/*****************************************add sprint modal ends***********************************************/
	
				
					
/*****************************************submit event starts***********************************************/					
						$("#submit_sprint").on("click",function(event){
						 if (!$('#add_sprint').valid()){
							    event.preventDefault();
							    event.stopImmediatePropagation();
							    return false;
						 }
						 else
						 {
						 
							 var start_date=$('#sprint_start').val();
							 var end_date=$('#sprint_end').val();
							 var project_start_date="{{session.current_project.get.startDate|date:'m/d/Y'}}";
							 var project_end_date="{{session.current_project.get.endDate|date:'m/d/Y'}}";
							 
							 var project_startdate=project_start_date;
							 var project_enddate=project_end_date;
							 
						
							 start_date =Date.parse(start_date);
							 end_date=Date.parse(end_date);
							 project_start_date=Date.parse(project_start_date);
							 project_end_date =Date.parse(project_end_date);
							 
							 
							// alert(release_end_date);
							
							//to check if sprint start date is before project start date
							
							 if(start_date < project_start_date && start_date!='')
							 {
								 
									$('#date_error').text("Start date cannot before project start date("+project_startdate+").")
									event.preventDefault();
									 event.stopImmediatePropagation();
									 return false;
									 
								 
							 }
							 else
							 
							//to check if sprint start date is after project end date	 
							 if (start_date > project_end_date && start_date!='')
							 {
									 
									$('#date_error').text("Start date cannot be after project end date("+project_enddate+").")
									event.preventDefault();
									 event.stopImmediatePropagation();
									 return false;
									 
								 
							 }
							 else
								 
							//to check if sprint end date before project start date 
								if (end_date < project_start_date && end_date !='' )
								 {
										 
										$('#date_error').text("End Date cannot be before project start date("+project_startdate+").")
										event.preventDefault();
										 event.stopImmediatePropagation();
										 return false;
										 
									 
								 }
								 
								 else
									 
							//to check if sprint end date is after project end date
								 if (end_date > project_end_date && end_date !='')
								 {
										 
										$('#date_error').text("End date cannot be after project end date("+project_enddate+").")
										event.preventDefault();
										 event.stopImmediatePropagation();
										 return false;
										 
									 
								 }
							 else
							/* 	 
							//to check if 
								if (end_date > project_end_date && start_date > project_end_date && end_date !='' && start_date!='')
									 {
											 
											$('#date_error').text("Start date & end date cannot be after project end date("+project_enddate+").")
											event.preventDefault();
											 event.stopImmediatePropagation();
											 return false;
											 
										 
									 } 
								 else 
								 
								 
								if (end_date < project_start_date && start_date < project_start_date && end_date !='' && start_date!='')
											 {
													 
													$('#date_error').text("Start date & end date cannot be before project start date("+project_startdate+").")
													event.preventDefault();
													 event.stopImmediatePropagation();
													 return false;
													 
												 
											 } 
											 
								else*/
								
								//to check if sprint start date is after sprint end date
									if(start_date > end_date)
									{
										$('#date_error').text("Start date cannot be after end date.")
										event.preventDefault();
										 event.stopImmediatePropagation();
										 return false;
										
									}
							
								
								if(end_date > release_end_date)
										{
											$('#date_error').text("End date cannot be after release date.")
											event.preventDefault();
											 event.stopImmediatePropagation();
											 return false;
											
										}
							 else
							
								 {
							 
							
							 
							 $('#date_error').text("");
							 $.post( "/sprint", $("#add_sprint").serialize())
						  		.done(function( data ) {
						  			if (data!="true"){
						  				alert("Sprint cannot be added.");
						  				return false
						  			} 
						  		//	$("#backlog_form").reset();
						  		else
						  			{
						  			alert("Sprint added successfully.");
						  		
						  			$('#tasks_sprints').load('/sprint #tasks_sprints', function(result) {
						  			
						  				
						  				$(".table").each(function(){
											if (!$(this).find("tr.find_empty").length){
											a=$(this).find("tbody")[0];
											$(a).append("<tr><td colspan='10' align='center'>There are no tasks in the sprint</td></tr>")
											}
											
										})
						  			});
									$('#sprint_dropdown').load('/sprint #sprint_dropdown', function(result) {
						  			
						  			});
						  			
						  			}
						  			
						  			 
						  		
						  		});
							
							 }	
						 }	
								
						})
					
/*****************************************submit event ends***********************************************/						
			/* 		$("#submit_sprint").on("click",function(){
						$.post( "/sprint", $("#add_sprint").serialize())
				  		.done(function( data ) {
				  			if (data!="true"){
				  				alert("Something Went Wrong");
				  				return false
				  			} 
				  		})
					});
						 */
				  			
/*****************************************modal hide starts***********************************************/
				  			$('#add-sprint-modal').on('hidden.bs.modal', function(e)
								    { 
									//	alert("hey");
										 $('#date_error').text("");
										$(this).removeData('bs.modal');
										$(this).find('form')[0].reset();
										sprint_validator.resetForm();
									/* 	$('#tasks_sprints').load('/sprint #tasks_sprints', function(result) {
						  				    //var variable = $('#edit_permissions').html();
						  				});
								 */
								    }) ;
							
				  		
					
					$('#edit-issue-modal').on('hidden.bs.modal', function(e)
						    { 
						        $(this).removeData();
						       // console.log(window.location.href);
						       
						        
						        
						    }) ;
					
/*****************************************submit event ends***********************************************/		
/******************************************for complete sprint dropdown starts***********************************************/

$(document).on("click", ".sprint_status_link",function() {
					
						var sprint_key=$(this).find('.sprint_key').val();
					
						var status= $(this).text()
						
						$.post( "/sprint/status",{key : sprint_key , status : status},function( data ) {
							
							  //alert(data);
							if (data!="true"){
				  				/* alert("Sprint status cannot be updated as all the task within the sprint are not completed.Please complete all task to complete a sprint.");
				  				return false */
				  				
								$.get('/sprint/tasklist',{key : sprint_key},function(data){
									
									console.log(data);
									$('#tr_content').html(data);
									
									$('#pending-task-modal').modal('show');
								});
				  				
				  			}  
							
							else {
				  				
				  				alert("Sprint status updated successfully.");
					  			$('#tasks_sprints').load('/sprint #tasks_sprints', function(result) {
					  				$(".table").each(function(){
										if (!$(this).find("tr.find_empty").length){
										a=$(this).find("tbody")[0];
										$(a).append("<tr><td colspan='10' align='center'>There are no tasks in the sprint</td></tr>")
										}
										
									})
					  			});
					  			
					  			
				  				
				  		}	
						
						});
					});

/****************************************complete sprint dropdown ends******************************************/

	
 
 
 
 /************************************************************add sprint page ends******************************************************/
 
 /**************************************************************edit sprint start******************************************************/
 /***************************************length of week starts*************************************/
	  
	  var sprint_start=$('#start').val();
      var sprint_end=$('#end').val();
      
      if(sprint_start != '' & sprint_end != '')
      {
      	secs=(new Date(sprint_end)).getTime()/1000-(new Date(sprint_start)).getTime()/1000
      	secs=secs/60/60/24;
      	if (secs>=7){
      		week=parseInt(secs/7);
      		days=secs%6;
      		$("#length").val(week+" weeks "+days+" days")
      	}
      	else {
      		if(secs==0){
      		$("#length").val("1 Day")
      		} else {
      			secs=secs+1;
      			$("#length").val(secs+" Days")
      		}
      	 }					
      }			
					
/***************************************length of week ends*************************************/		
/****************************icon click starts*****************************************************/
$('.form-group').find('.open-datetimepicker').on('click', function(){
					    $('#start').trigger('focus');
					});
					

$('.form-group').find('.open-datetimepicker1').on('click', function(){
					    $('#end').trigger('focus');
					});

					
/******************************icon click ends*******************************************/					
/************************************sprint validation starts***************************************/
					
					var sprint_validator=   $("#edit_sprint").validate({
						      rules: {
						    	  name: 
						    	  {
						           		 required: true
						          },
						          start: 
						    	  {
						           		 required: true
						          },
						          end: 
						    	  {
						           		 required: true
						          },
						          desc: 
						          {
							      		 required: true
							      },
							   
								  new_workinghours: 
								  {
										 required: true
										
									
								  }
								
					   
						         },
						         messages: 
						         {
						        	 name: 
						           {
						             required: "Please enter sprint name."
						           },
						           start: 
							    	{
							           		 required: "Please enter start date."
							        },
							        end: 
							    	{
							           		 required: "Please enter end date."
							       },
						           desc: 
						           {
						             required: "Please enter sprint description."
						           },
						       
							       new_workinghours: 
							       {
							             required: "Please enter working hours."
							       }
							   
						           
						         }
						     });
/***************************************sprint validation ends**********************************************/
					
/*********************************datepicker function starts*******************************************/					
					
					$('body').on('focus',"#start,#start_edit", function(){
					    $(this).datepicker({
							format: 'mm/dd/yyyy',
							//startDate: '0d'
						});
					});
					$('body').on('focus',"#end,#end_edit", function(){
					    $(this).datepicker({
							format: 'mm/dd/yyyy',
							//startDate: '0d'
						});
					    
					});
					$('.datepicker').datepicker({
						format: 'mm/dd/yyyy',
						//startDate: '0d',
						autoclose:true
					});
					$('.datepicker').datepicker()
				    .on('changeDate', function(e) {
				        $('.datepicker').datepicker('hide');
				    });
					
					
				 
					
					
					$('#end').datepicker()
				    .on('changeDate', function(e) {
				    	if ($('#start').val()!=""){
					        start=$('#start').val();
					        end=$('#end').val();
					        secs=(new Date(end)).getTime()/1000-(new Date(start)).getTime()/1000
					        secs=secs/60/60/24;
					        if (secs>=7){
					        	week=parseInt(secs/7);
					        	days=secs%6;
					        	$("#length").val(week+" weeks "+days+" days")
					        }
					        else {
					        	if(secs==0){
					        		$("#length").val("1 Day")
					        	} else {
					        		secs=secs+1;
					        	$("#length").val(secs+" Days")
					        	}
					        }
				    	}
				    });
					$('#start').datepicker()
				    .on('changeDate', function(e) {
				    	if ($('#end').val()!=""){
				    		start=$('#start').val();
					        end=$('#end').val();
					        secs=(new Date(end)).getTime()/1000-(new Date(start)).getTime()/1000
					        secs=secs/60/60/24;
					        if (secs>=7){
					        	week=parseInt(secs/7);
					        	days=secs%6;
					        	$("#length").val(week+" weeks "+days+" days")
					        }
					        else {
					        	if(secs==0){
					        		$("#length").val("1 Day")
					        	} else {
					        		secs=secs+1;
					        	$("#length").val(secs+" Days")
					        	}
					        }
				    	}
				    });
					
					
					
/*********************************datepicker function ends*******************************************/	
					/*$("#add-issue").click(function(e) {
						$('#add-issue-modal').modal('show');
					});*/
				
/*********************************submit function starts*******************************************/
					$("#submit_sprint").on("click",function(event){
						console.log("comes inside");
						 if (!$('#edit_sprint').valid()){
							    console.log("comes inside if");
							    event.preventDefault();
							    event.stopImmediatePropagation();
							    return false;
						 }
						 else
						 {
						 console.log("comes inside else");
						 var start_date=$('#start').val();
						 var end_date=$('#end').val();
					 	 var project_start_date="{{session.current_project.get.startDate|date:'m/d/Y'}}";
						 var project_end_date="{{session.current_project.get.endDate|date:'m/d/Y'}}";
						 
						 var project_startdate=project_start_date;
						 var project_enddate=project_end_date;
						 
						 start_date =Date.parse(start_date);
						 end_date=Date.parse(end_date);
						 project_start_date=Date.parse(project_start_date);
						 project_end_date =Date.parse(project_end_date);
						 
						 
						//to check if sprint start date is before project start date
							
						 if(start_date < project_start_date && start_date!='')
						 {
							 
								$('#date_error').text("Start date cannot before project start date("+project_startdate+").")
								event.preventDefault();
								 event.stopImmediatePropagation();
								 return false;
								 
							 
						 }
						 else
						 
						//to check if sprint start date is after project end date	 
						 if (start_date > project_end_date && start_date!='')
						 {
								 
								$('#date_error').text("Start date cannot be after project end date("+project_enddate+").")
								event.preventDefault();
								 event.stopImmediatePropagation();
								 return false;
								 
							 
						 }
						 else
							 
						//to check if sprint end date before project start date 
							if (end_date < project_start_date && end_date !='' )
							 {
									 
									$('#date_error').text("End Date cannot be before project start date("+project_startdate+").")
									event.preventDefault();
									 event.stopImmediatePropagation();
									 return false;
									 
								 
							 }
							 
							 else
								 
						//to check if sprint end date is after project end date
							 if (end_date > project_end_date && end_date !='')
							 {
									 
									$('#date_error').text("End date cannot be after project end date("+project_enddate+").")
									event.preventDefault();
									 event.stopImmediatePropagation();
									 return false;
									 
								 
							 }
						 else
						/* 	 
						//to check if 
							if (end_date > project_end_date && start_date > project_end_date && end_date !='' && start_date!='')
								 {
										 
										$('#date_error').text("Start date & end date cannot be after project end date("+project_enddate+").")
										event.preventDefault();
										 event.stopImmediatePropagation();
										 return false;
										 
									 
								 } 
							 else 
							 
							 
							if (end_date < project_start_date && start_date < project_start_date && end_date !='' && start_date!='')
										 {
												 
												$('#date_error').text("Start date & end date cannot be before project start date("+project_startdate+").")
												event.preventDefault();
												 event.stopImmediatePropagation();
												 return false;
												 
											 
										 } 
										 
							else*/
							
							//to check if sprint start date is after sprint end date
								if(start_date > end_date)
								{
									$('#date_error').text("Start date cannot be after end date.")
									event.preventDefault();
									 event.stopImmediatePropagation();
									 return false;
									
								}
						 else
						
							 {
							 
							 $('#date_error').text("");
							 
							 $.post( "/sprint/edit", $("#edit_sprint").serialize())
						  		.done(function( data ) {
						  			if (data!="true"){
						  				alert("Something Went Wrong");
						  				return false
						  			} 
						  		//	$("#backlog_form").reset();
						  			
						  			
						  			 
						  		
						  		});
							
							 }
						 	}		
								
						})
					
						
			/* 		$("#submit_sprint").on("click",function(){
						$.post( "/sprint", $("#add_sprint").serialize())
				  		.done(function( data ) {
				  			if (data!="true"){
				  				alert("Something Went Wrong");
				  				return false
				  			} 
				  		})
					});
						 */
				  			
/*********************************submit function ends*******************************************/
 
/*********************************close modal starts*******************************************/
		$('#edit-sprint-modal').on('hidden.bs.modal', function(e)
								    { 
									$('#date_error').text("");
										$(this).removeData('bs.modal');
										//$(this).find('form')[0].reset();
										//sprint_validator.resetForm();
										$('#tasks_sprints').load('/sprint #tasks_sprints', function(result) {
						  				    //var variable = $('#edit_permissions').html();
						  				$(".table").each(function(){
												if (!$(this).find("tr.find_empty").length){
												a=$(this).find("tbody")[0];
												$(a).append("<tr><td colspan='10' align='center'>There are no tasks in the sprint</td></tr>")
												}
												
											})
											
										
										
										});
										
										$('#sprint_dropdown').load('/sprint #sprint_dropdown', function(result) {
								  			
							  			});
								
								    }) ;
							
/*********************************close modal ends*******************************************/		

 /**************************************************************edit sprint ends******************************************************/

/******************************************************add & edit task start******************************************************/
/***************************************sprint and user story data fetch starts************************************************/
		
	var sprint;
	sprint=$('#sprint_name').val();
	 var sprint_start_date;
	 var sprint_end_date;
	 
	if (sprint != 'None')
	{
	
		sprint=$('#sprint_name').val(); 
		$.post( "/sprint_info?key="+sprint+"")
  		.done(function( data ) {
  			//alert(data);
			console.log(data);
			var str = "\""+data+"\"";
			//var myarray = str.split('(');
				
			sprint_start_date= str.substring(2, 12);
			
			
			sprint_end_date= str.substring(16, 26);
				
  		});
			
		
		 $.get("/dropdown_userstory?key="+sprint+"", function(data){
	            //alert( data );
	            $("#load_user_story").html(data);
	            
	            
	        });
	
	
	
	}
	/*else
	 	{
		 $("#load_user_story").html("<select name='user_story' id='user_story' class='form-control add-task-textbox apm-modal-textbox'><option value='None'>None</option></select>");
		} */

/***************************************sprint and user story data fetch ends************************************************/	
	 
	
/****************************************icon click starts*******************************************************/	
	
	$('.form-group').find('.open-datetimepicker').on('click', function(){
	    $('#start').trigger('focus');
	});

	$('.form-group').find('.open-datetimepicker1').on('click', function(){
	    $('#end').trigger('focus');
	});
	
/****************************************icon click ends*****************************************************/

 /****************************************datepicker starts*****************************************************/
	$('body').on('focus',"#start,#start_edit", function(){
	    $(this).datepicker({
			format: 'dd/mm/yyyy',
			startDate: '0d'
		});
	});
	$('body').on('focus',"#end,#end_edit", function(){
	    $(this).datepicker({
			format: 'dd/mm/yyyy',
			startDate: '0d'
		});
	});
	
	$('.datepicker').datepicker({
		format: 'mm/dd/yyyy',
		startDate: '0d',
		autoclose:true
	});
/****************************************datepicker ends*****************************************************/
	
	
/****************************************complexity points starts*****************************************************/
	$("#complex_pt option").filter(function() {
        return $(this).val() == $("#est_efforts").val();
    }).attr('selected', true);

    $(document).on("change","#complex_pt", function() {

        $("#est_efforts").val($(this).find("option:selected").attr("data"));
    });
    
/****************************************complexity points ends*****************************************************/


/****************************************task validation starts*****************************************************/
	var task_validator=   $("#task_form").validate({
		      rules: {
		    	  name: 
		    	  {
		           		 required: true
		          },
		          desc: 
		          {
			      		 required: true
			      },
			
				  complexity: 
				  {
						 required: true
						
					
				  },
				  actual_efforts:
				  {
						 required: true,
						 number:true
						
					
				  }
	   
		         },
		         messages: 
		         {
		        	 name: 
		           {
		             required: "Please enter task title."
		           },
		           desc: 
		           {
		             required: "Please enter task description."
		           },
		         
			       complexity: 
			       {
			             required: "Please select complexity."
			       },
			       actual_efforts:
			       {
			             required: "Please enter estimated efforts.",
			             number:"Please enter number only."
			       }
		         }
		     });
	
/****************************************task validation ends*****************************************************/

/****************************************sprint data fetch starts*****************************************************/
	
	$(document).on('change','#sprint_name', function (e) {
		
		sprint=$('#sprint_name').val(); 
		$.post( "/sprint_info?key="+sprint+"")
  		.done(function( data ) {
  			//alert(data);
			console.log(data);
			var str = data;
			//var myarray = str.split('(');
				
			sprint_start_date= str.substring(2, 12);
			
			
			sprint_end_date= str.substring(16, 26);
				
  		});
			
		
		 $.get("/dropdown_userstory?key="+sprint+"", function(data){
	            //alert( data );
	            $("#load_user_story").html(data);
	            
	           
	        });
	
	
		});

	
/****************************************sprint data fetch ends*****************************************************/ 
 /****************************************edit form submit starts*****************************************************/
		$(document).on("click","#submit_task",function(event){
			
			 if (!$('#task_form').valid()){
				    event.preventDefault();
				    event.stopImmediatePropagation();
				    return false;
			 }
			 
			 else
			 {
				 
				
				$.post( "/task/edittask", $("#task_form").serialize())
	  			.done(function( data ) {
	  			if (data!="true"){
	  				alert("Something Went Wrong");
	  				return false
	  			}
	  			else
  				{
	  				$(this).find('form')[0].reset();
  				
  				}
	  		 });
		 }

					
	})
				
/****************************************edit form submit ends*****************************************************/	
 
 	
/****************************************add form submit starts*****************************************************/
$(document).on("click","#submit_item",function(event){
						 if (!$('#task_form').valid()){
							    event.preventDefault();
							    event.stopImmediatePropagation();
							    return false;
						 }
						 
						 else{
							 
							 $('#date_error').text("");
								$.post( "/task/addtask", $("#task_form").serialize())
						  		.done(function( data ) {
						  			console.log(data);
						  			if (data!="true"){
						  				alert("Something Went Wrong");
						  				return false
						  			} 
						  			else
						  				{
						  			
						  				$(this).find('form')[0].reset();
						  				console.log('out');
						  				}
						  		});
						
							 }
							
								
						})
						
/****************************************add form submit ends*****************************************************/	
 
 
/****************************************hide issue modal starts*****************************************************/
						
					$('#add-issue-modal').on('hidden.bs.modal', function(e)
									    { 
											$('#date_error').text("");
									        $(this).removeData('bs.modal');
									       // $(this).find('form')[0].reset();
									        
									        var s= window.location.href.split(".com/").pop();
									        if (s.indexOf("?sprint_key")>1)
									        {
									        	var sprintkey = window.location.href.split(".com/sprint?sprint_key=").pop();
									        	$('#tasks_sprints').load('/sprint?sprint_key='+sprintkey+' #tasks_sprints', function(result) {
							  				    
							  					});
									        	
									        }
									        else
									        {
									        	$('#tasks_sprints').load('/sprint #tasks_sprints', function(result) {
								  				    //var variable = $('#edit_permissions').html();
								  					});
										        	 $('#sprint_dropdown').load('/sprint #sprint_dropdown', function(result) {
										  			
									  				}); 
									        }
									  
										
									    }) ;	
/****************************************hide issue modal ends*****************************************************/

		
 
 /*****************************************************add & edit task ends*******************************************************/
 
 /**************************************************sprint status start******************************************************/
 $(document).on("click","#move_sprint_tasks",function(){
		$.post( '/sprint/tasklist', $("#update_form").serialize())
			.done(function( data ) {
				if (data!="true"){
					alert("Tasks cannot be moved.");
					return false
				} else {
					
					/* alert("Task updated."); */
					
				}
			});
			
			
				
				
			})
			
			
				$('#pending-task-modal').on('hidden.bs.modal', function(e)
					    { 
					        $(this).removeData('bs.modal');
					        
					        $('#tasks_sprints').load('/sprint #tasks_sprints', function(result) {
					        //	$("#details").hide();
					        	
					  
					        	
			  				});
					  
					        
					    }) ;
 /**************************************************sprint status ends******************************************************* **/
 
 
 
/****************************************************move task starts******************************************************/

$(document).on("click","#movetask",function(){
	$.post( '/task/movetask', $("#update_form").serialize())
		.done(function( data ) {
			if (data!="true"){
				alert("Task cannot be moved.");
				return false
			} else {
				
				/* alert("Task updated."); */
				
			}
		});
		
		
			
			
		})
		
		
			$('#move-issue-modal').on('hidden.bs.modal', function(e)
				    { 
				        $(this).removeData('bs.modal');
				        
				        $('#tasks_sprints').load('/sprint #tasks_sprints', function(result) {
				        //	$("#details").hide();
				        	
				  
				        	
		  				});
				  
				        
				    }) ; 
/*****************************************************move task ends*******************************************************/ 
 });