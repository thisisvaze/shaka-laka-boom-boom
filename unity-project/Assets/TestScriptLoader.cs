using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TestScriptLoader : MonoBehaviour
{

    void Start()
    {
        Destroy(GetComponent<TrackObjects>());
        Destroy(GetComponent<CaptureImage>());
        Destroy(GetComponent<CaptureVoiceIntent>());
        GetComponent<GenerateFacts>();

        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
