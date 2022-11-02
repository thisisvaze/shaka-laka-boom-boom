using UnityEngine;
using System;
using System.Net;
using UnityEngine.Networking;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine.Windows.WebCam;
using TMPro;
using System.Security.Cryptography.X509Certificates;
using System.Security.Cryptography;
using System.Runtime.InteropServices;
using Microsoft.MixedReality.Toolkit;
using Microsoft.MixedReality.Toolkit.Subsystems;
using Microsoft.MixedReality.Toolkit.SpatialManipulation;
using Microsoft.MixedReality.Toolkit.Input;
using UnityEngine.Windows.Speech;
using UnityEngine.UI;
using NativeWebSocket;
using System.Threading;
using System.Threading.Tasks;


public class SketchTo3D : MonoBehaviour

{   List<string> generatedObjects = new List<string>();
    public string SERVER_IP = "http://localhost:8000/slbb";
    public Dictionary<string,string> modelState = new Dictionary<string, string>();
   
    [Serializable]
    public class LabelInfo
    {
        public string name;
        public string x;
        public string y;
    }
    // Use this for initialization
    [Serializable]
    public class Picture
    {
        public string PhotoFileName;
    }

    [Serializable]
    public class ModelInfo
    {
        public string model_url;
    }

     [Serializable]
    public class JsonModelDatabase
    {
        public string data;
        public string scale;
    }

    public static class JsonHelper
    {
        public static T[] FromJson<T>(string json)
        {
            Wrapper<T> wrapper = JsonUtility.FromJson<Wrapper<T>>(json);
            return wrapper.Items;
        }
        public static string ToJson<T>(T[] array)
        {
            Wrapper<T> wrapper = new Wrapper<T>();
            wrapper.Items = array;
            return JsonUtility.ToJson(wrapper);
        }
        public static string ToJson<T>(T[] array, bool prettyPrint)
        {
            Wrapper<T> wrapper = new Wrapper<T>();
            wrapper.Items = array;
            return JsonUtility.ToJson(wrapper, prettyPrint);
        }
        [Serializable]
        private class Wrapper<T>
        {
            public T[] Items;
        }
    }

    void Start()

    
    { 
     StartCoroutine(Get3DModelFromSketch());
    }



        void generateCustomFromURL(string url, float scale)
    {
        Debug.Log("Generate GLTF");
        ImportGLTF(url, scale);
    }

    void ImportGLTF(string filepath, float scale) {
        var empty = new GameObject(); 
        var gltf = empty.AddComponent<GLTFast.GltfAsset>();
        gltf.url = filepath;

        Vector3 forwardPosition = Camera.main.transform.rotation * Vector3.forward*0.5f;
        Vector3 finalPosition = Camera.main.transform.position + forwardPosition;
        gltf.transform.localPosition = finalPosition;
        //gltf.transform.localScale = new Vector3(1f, 1f, 1f);
        empty.transform.localScale = new Vector3(scale, scale, scale);
        empty.AddComponent<BoxCollider>();
        empty.AddComponent<BoundsControl>();
        empty.AddComponent<ObjectManipulator>();
        empty.AddComponent<ConstraintManager>();
        
        Debug.Log("Generatated the 3D object");
    }

    IEnumerator Get3DModelFromSketch(){
         // Sketch to 3D model
        UnityWebRequest req3 = UnityWebRequest.Post(SERVER_IP, "");
        yield return req3.SendWebRequest();
        if (req3.result != UnityWebRequest.Result.Success)
        {
            if (req3.isNetworkError || req3.isHttpError || req3.isNetworkError)
                print("Error: " + req3.error);
            Debug.Log(req3.downloadHandler.text);
        }
        else
        {   Debug.Log(req3.downloadHandler.text);
            //JsonModelDatabase modelDatabase = JsonHelper.FromJson<JsonModelDatabase>(req3.downloadHandler.text);
            ModelInfo[] info = JsonHelper.FromJson<ModelInfo>(req3.downloadHandler.text);
            Debug.Log(info[0]);
            String a = info[0].model_url;
            float objectScale = 0.01f;
            if(info[0].model_url!="none"){
                if(generatedObjects.Contains(info[0].model_url) == false)
  
                    {
                    //ambulance 0.01f
                    //ant 0.1f
                    //airplane 0.001f
                    //backpack 0.001f
                switch(info[0].model_url){
                    case "ambulance": objectScale = 0.001f;
                    break;
                    case "apple": objectScale = 0.005f;
                    break;
                    case "ant": objectScale = 0.01f;
                    break;
                    case "airplane": objectScale = 0.001f;
                    break;
                    case "backpack": objectScale = 0.001f;
                    break;
                } 
                        
                    generateCustomFromURL(Application.dataPath + "/Resources/"+info[0].model_url+".glb", objectScale);
                    generatedObjects.Add(info[0].model_url);
                    }
            }
            else{
                Debug.Log("No object detected yet");
            }
        }
        yield return new WaitForSeconds(1);
        StartCoroutine(Get3DModelFromSketch());

    }

}


    // private string Base64Encode(string plainText)
    // {
    //     var plainTextBytes = System.Text.Encoding.UTF8.GetBytes(plainText);
    //     return System.Convert.ToBase64String(plainTextBytes);
    // }
    