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
public class LightsData
{
    public string id;
    public float x, y, z;

    public bool state;

    public bool needsRotation;

    public LightsData(string id, float x, float y, float z, bool state, bool needsRotation)
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

[Serializable]
public class TrafficData
{
    public List<LightsData> positions;

    public TrafficData() => this.positions = new List<LightsData>();
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

    private int randomCar;

    AgentsData agentsData;

    TrafficData lightsData;

    Dictionary<string, GameObject> agents;

    Dictionary<string, GameObject> lights;

    Dictionary<string, Vector3> prevPositions, currPositions;

    Dictionary<string, Vector3> lprevPositions, lcurrPositions;

    bool updated = false, started = false, lightsStarted = false;

    
    //public GameObject agentPrefab, lightPrefab, floor;
    public GameObject lightPrefab, floor;
    public int NAgents, width, height;
    public float timeToUpdate = 5.0f;
    private float timer, dt;

    void Start()
    {
        agentsData = new AgentsData();
        lightsData = new TrafficData();

        prevPositions = new Dictionary<string, Vector3>();
        currPositions = new Dictionary<string, Vector3>();

        agents = new Dictionary<string, GameObject>();
        lights = new Dictionary<string, GameObject>();

        floor.transform.localScale = new Vector3((float)width/10, 1, (float)height/10);
        floor.transform.localPosition = new Vector3((float)width/2-0.5f, 0, (float)height/2-0.5f);
        
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

            foreach(var agent in currPositions)
            {
                Vector3 currentPosition = agent.Value;
                Vector3 previousPosition = prevPositions[agent.Key];

                Vector3 interpolated = Vector3.Lerp(previousPosition, currentPosition, dt);
                Vector3 direction = currentPosition - interpolated;

                agents[agent.Key].transform.localPosition = interpolated;
                if(direction != Vector3.zero) agents[agent.Key].transform.rotation = Quaternion.LookRotation(direction);
            }

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

        form.AddField("NAgents", NAgents.ToString());
        form.AddField("width", width.ToString());
        form.AddField("height", height.ToString());

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

                    if(!started)
                    {
                        prevPositions[agent.id] = newAgentPosition;
                        randomCar=UnityEngine.Random.Range(0,carPrefabs.Count());
                        agents[agent.id] = Instantiate(carPrefabs[randomCar], newAgentPosition, Quaternion.identity);
                        //agents[agent.id] = Instantiate(agentPrefab, newAgentPosition, Quaternion.identity);
                    }
                    else
                    {
                        Vector3 currentPosition = new Vector3();
                        if(currPositions.TryGetValue(agent.id, out currentPosition))
                            prevPositions[agent.id] = currentPosition;
                        currPositions[agent.id] = newAgentPosition;
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
            lightsData = JsonUtility.FromJson<TrafficData>(www.downloadHandler.text);

            Debug.Log(www.downloadHandler.text);

            foreach(LightsData light in lightsData.positions)
            {
                Vector3 newAgentPosition = new Vector3(light.x, light.y, light.z);
                 if(!lightsStarted)
                    {
                        
                        
                        
                        
                        if (light.needsRotation && light.x > 15 && light.z > 20)
                        {
                            lights[light.id] = Instantiate(lightPrefab, new Vector3(light.x- 0.5f, light.y, light.z - 0.5f), Quaternion.Euler(0,90,0));
                        }
                        else
                        {
                            if (light.needsRotation)
                            {
                                lights[light.id] = Instantiate(lightPrefab, new Vector3(light.x, light.y, light.z + 0.5f), Quaternion.Euler(0,90,0));
                            }
                            else
                            {
                            lights[light.id] = Instantiate(lightPrefab, new Vector3(light.x-0.5f, light.y, light.z), Quaternion.identity);
                            }
                        }
                        
                        
                        
                        
                        
                    }
                    else
                    {
                        lights[light.id].GetComponent<LightBehavior>().toggleLights(light.state);
                    }

                    
        }
        if(!lightsStarted) lightsStarted = true;
    }
}}