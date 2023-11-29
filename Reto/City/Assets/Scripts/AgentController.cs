using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

[Serializable]
public class AgentData
{
    public string id;
    public float x, y, z;

    public AgentData(string id, float x, float y, float z)
    {
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
    }
}

[Serializable]
public class LightData
{
    public string id;
    public float x, y, z;

    public bool state;

    public bool needsRotation;

    public LightData(string id, float x, float y, float z, bool state, bool needsRotation)
    {
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
        this.state = state;
        this.needsRotation = needsRotation;
    }
}

[Serializable]
public class AgentsData
{
    public List<AgentData> positions;

    public AgentsData() => this.positions = new List<AgentData>();
}
// Clase del agente semáforo luz prueba
[Serializable]
public class TLightData
{
    public string id;
    public float x, y, z;
    public bool state;

    public TLightData(string id, float x, float y, float z, bool state)
    {
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
        this.state = state;
    }
}
[Serializable]
public class TLightsData
{
    public List<TLightData> positions;

    public TLightsData() => this.positions = new List<TLightData>();
}


public class AgentController : MonoBehaviour
{
    // private string url = "https://agents.us-south.cf.appdomain.cloud/";
    string serverUrl = "http://localhost:8585";
    string getAgentsEndpoint = "/getAgents";
    string getLightsEndpoint = "/getLights";
    
    string sendConfigEndpoint = "/init";
    string updateEndpoint = "/update";

    public List<GameObject> carPrefabs;

    public GameObject luz; //luz de prueba
    private int randomCar;

    AgentsData agentsData;

    TLightsData tlightsData;

    Dictionary<string, GameObject> agents;

    Dictionary<string, GameObject> lights;

    Dictionary<string, Vector3> prevPositions, currPositions;

    Dictionary<string, Vector3> lprevPositions, lcurrPositions;

    bool updated = false, started = false, tlightsStarted = false;

    
    //public GameObject agentPrefab, lightPrefab, floor;
    public GameObject lightPrefab;
    public int timetogenerate, timecounter;
    public float timeToUpdate = 1.0f;
    private float timer, dt;

    void Start()
    {
        agentsData = new AgentsData();
        tlightsData = new TLightsData();

        prevPositions = new Dictionary<string, Vector3>();
        currPositions = new Dictionary<string, Vector3>();

        agents = new Dictionary<string, GameObject>();
        lights = new Dictionary<string, GameObject>();

        
        
        timer = timeToUpdate;

        StartCoroutine(SendConfiguration());
    }

    private void Update() 
    {
        if(timer < 0)
        {
            timer = timeToUpdate;
            updated = false;
            StartCoroutine(UpdateSimulation());
        }

        if (updated)
        {
            timer -= Time.deltaTime;
            dt = 1.0f - (timer / timeToUpdate);

            
            // float t = (timer / timeToUpdate);
            // dt = t * t * ( 3f - 2f*t);
        }
    }
 
    IEnumerator UpdateSimulation()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + updateEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            StartCoroutine(GetAgentsData());
            StartCoroutine(GetLightsData());
            
        }
    }

    IEnumerator SendConfiguration()
    {
        WWWForm form = new WWWForm();

        form.AddField("timetogenerate", timetogenerate.ToString());
        form.AddField("timecounter", timecounter.ToString());
        

        UnityWebRequest www = UnityWebRequest.Post(serverUrl + sendConfigEndpoint, form);
        www.SetRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            Debug.Log("Configuration upload complete!");
            Debug.Log("Getting Agents positions");
            
            StartCoroutine(GetAgentsData());
            StartCoroutine(GetLightsData());
            
        }
        //yield return 0;
    }

    IEnumerator GetAgentsData() 
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getAgentsEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            agentsData = JsonUtility.FromJson<AgentsData>(www.downloadHandler.text);

            foreach(AgentData agent in agentsData.positions)
            {
                Vector3 newAgentPosition = new Vector3(agent.x, agent.y, agent.z);

                    if(!agents.ContainsKey(agent.id))
                    {
                        prevPositions[agent.id] = newAgentPosition;
                        randomCar=UnityEngine.Random.Range(0,carPrefabs.Count());
                        agents[agent.id] = Instantiate(carPrefabs[randomCar], Vector3.zero, Quaternion.identity);
                        move carmove=agents[agent.id].GetComponent<move>();//obtiene el script para el carro
                        carmove.Positions(newAgentPosition);
                        carmove.Positions(newAgentPosition);//envia la posicion inicial del carro
                        //agents[agent.id] = Instantiate(agentPrefab, newAgentPosition, Quaternion.identity);
                    }
                    else
                    {
                        move carmove=agents[agent.id].GetComponent<move>();//obtiene el script para el carro
                        carmove.Positions(newAgentPosition);//envia la posicion inicial del carro
                    }
            }

            updated = true;
            if(!started) started = true;
        }
    }

    IEnumerator GetLightsData() 
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getLightsEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            tlightsData = JsonUtility.FromJson<TLightsData>(www.downloadHandler.text);

            Debug.Log(www.downloadHandler.text);

            foreach(TLightData light in tlightsData.positions)
            {
                
                 if(!tlightsStarted)
                    {
                     Vector3 newAgentPosition = new Vector3(light.x, light.y, light.z);
                     lights[light.id]=Instantiate(luz, newAgentPosition, Quaternion.identity); //luz de prueba
                     lights[light.id].name=light.id;
                    }
                    else{
                        if(light.state){
                        lights[light.id].GetComponent<Light>().color = Color.green;
                    } else {
                        lights[light.id].GetComponent<Light>().color = Color.red;
                    }
                    }   
                        
                        
                        
                        //if (light.needsRotation && light.x > 15 && light.z > 20)
                        //{
                         //   lights[light.id] = Instantiate(lightPrefab, new Vector3(light.x- 0.5f, light.y, light.z - 0.5f), Quaternion.Euler(0,90,0));
                        //}
                        //else
                        //{
                          //  if (light.needsRotation)
                            //{
                              //  lights[light.id] = Instantiate(lightPrefab, new Vector3(light.x, light.y, light.z + 0.5f), Quaternion.Euler(0,90,0));
                            //}
                            //else
                            //{
                            //lights[light.id] = Instantiate(lightPrefab, new Vector3(light.x-0.5f, light.y, light.z), Quaternion.identity);
                            //}
                        //}
                        
                        
                        
                        
                        
            }
                    //else
                    //{
                      //  lights[light.id].GetComponent<LightBehavior>().toggleLights(light.state);
                    //}
            if (!tlightsStarted)
            {
            tlightsStarted = true;
            }

                    
        }
        //if(!tlightsStarted) tlightsStarted = true;
    }
}


    