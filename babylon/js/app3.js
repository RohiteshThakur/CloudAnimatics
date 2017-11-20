/// <reference path="babylon.2.1.d.ts" />

var BjsApp = BjsApp || {};

BjsApp.init = function(){
	//get the canvas
	var canvas = document.getElementById('renderCanvas');
	
	//create a BabylonJS engine object
	var engine = new BABYLON.Engine(canvas, true);
	

	//var camera = new BABYLON.ArcRotateCamera('camera', 0, 0, 15, BABYLON.Vector3.Zero(), scene);
	//camera.attachControl(canvas);

	// Load blender scene
	BABYLON.SceneLoader.Load('', 'assets/Draw_in_Blender_ASG_With_PublicIPs.babylon', engine, function(scene){
		scene.executeWhenReady(function(){
			//Attach Camera
			var camera = new BABYLON.ArcRotateCamera('camera', 0, 0, 15, BABYLON.Vector3.Zero(), scene);
			camera.attachControl(canvas);
			//scene.activeCamera.attachControl(canvas);			

			engine.runRenderLoop(function(){
				scene.render();
			});
		});

	});

};
