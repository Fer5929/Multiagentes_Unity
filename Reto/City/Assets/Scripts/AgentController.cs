//S Fernanda Colomo F - A01781983
//Ian Luis Vázquez Morán - A01027225
/*Código para el comportamiento de los objetos en Unity y la conexión al servidor de flask
Principalmente se basa en obtener información del servidor tales como los agentes semáforo y Auto
para después instanciarlos en Unity y que se comporten como se definió en agent.py
También se encarga de actualizar la simulación gracias a Update.

*/
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

    public AgentData(string id, float x, float y, float z)//constructor del agente Carro
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

    public LightData(string id, float x, float y, float z, bool state, bool needsRotation)//constructor del agente semáforo
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
    public List<AgentData> positions;//lista de posiciones de los agentes

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
    public List<TLightData> positions;//lista de posiciones de los agentes semáforo

    public TLightsData() => this.positions = new List<TLightData>();
}


public class AgentController : MonoBehaviour
{
    // private string url = "https://agents.us-south.cf.appdomain.cloud/";
    //definición de endpoints
    string serverUrl = "http://localhost:8585";
    string getAgentsEndpoint = "/getAgents";
    string getLightsEndpoint = "/getLights";
    
    string sendConfigEndpoint = "/init";
    string updateEndpoint = "/update";

    public List<GameObject> carPrefabs;//lista de prefabs de los carros

    public GameObject luz; //luz de los semáforos
    private int randomCar;//así se elige un carro random cuando se inicializa

    AgentsData agentsData;

    TLightsData tlightsData;

    Dictionary<string, GameObject> agents;//diccionario de los agentes Carro

    Dictionary<string, GameObject> lights;//diccionario de los agentes semáforo

    Dictionary<string, Vector3> prevPositions, currPositions;//posiciones de los agentes para moverse

    Dictionary<string, Vector3> lprevPositions, lcurrPositions;

    bool updated = false, started = false, tlightsStarted = false;

    
    //public GameObject agentPrefab, lightPrefab, floor;
    public GameObject lightPrefab;
    public int timetogenerate, timecounter;//variables a modificar en el inspector
    public float timeToUpdate = 1.0f;//tiempo para actualizar la simulación
    private float timer, dt;

    void Start()
    {
       
        agentsData = new AgentsData();//se crea el objeto de los agentes
        tlightsData = new TLightsData();//se crea el objeto de los semáforos

         //se crean los diccionarios de agentes y de posiciones de los mismos
        prevPositions = new Dictionary<string, Vector3>();
        currPositions = new Dictionary<string, Vector3>();

        agents = new Dictionary<string, GameObject>();
        lights = new Dictionary<string, GameObject>();

        
        
        timer = timeToUpdate;

        StartCoroutine(SendConfiguration());//se empieza la corutina para enviar la configuración al servidor
    }

    private void Update() 
    {
        
        if(timer < 0)
        {
            timer = timeToUpdate;
            updated = false;
            StartCoroutine(UpdateSimulation());
            //se empieza la corutina para actualizar la simulación
        }

        if (updated)
        {
            timer -= Time.deltaTime;
            dt = 120.0f - (timer / timeToUpdate);


            

            // float t = (timer / timeToUpdate);
            // dt = t * t * ( 3f - 2f*t);
        }
    }
 
    IEnumerator UpdateSimulation()//actualiza la simulación llamando a getAgents y a GetLights
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

        //manda la información de la configuración al servidor para el modelo
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
            
            //ya que se mandó correctamente se empieza a obtener la información de los agentes Carro y semáforos
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
            List<string> idsPresentes = new List<string>();

            foreach(AgentData agent in agentsData.positions)
            {
                //por cada carro se obtiene una posición y se instancia en Unity
                Vector3 newAgentPosition = new Vector3(agent.x, 0, agent.z);

                    if(!agents.ContainsKey(agent.id))
                    {
                        //se verifica si el carro ya existe en el diccionario, si no se crea con sus respectivas posiciones
                        prevPositions[agent.id] = newAgentPosition;
                        randomCar=UnityEngine.Random.Range(0,carPrefabs.Count());
                        agents[agent.id] = Instantiate(carPrefabs[randomCar], Vector3.zero, Quaternion.identity);
                        agents[agent.id].name=randomCar + agent.id;
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
                    idsPresentes.Add(agent.id);
            }
            foreach (string agentID in agents.Keys.ToList())
            {
                if (!idsPresentes.Contains(agentID))
                {//si el carro llega a su destino se elimina del diccionario y de Unity
                    GameObject objetoAEliminar = agents[agentID];
                    for (int i=1; i<=4; i++){
                        string nombreObjetoAEliminar = objetoAEliminar.name + "wheel"+i;
                        Destroy(GameObject.Find(nombreObjetoAEliminar));
                    }
                    Destroy(agents[agentID]); // Eliminar el objeto de Unity correspondiente al ID no presente
                    agents.Remove(agentID);   // Eliminar el elemento del diccionario
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
                //por cada semaforo se instancia una luz en Unity
                
                 if(!tlightsStarted)
                    {
                     Vector3 newAgentPosition = new Vector3(light.x, light.y, light.z);
                     lights[light.id]=Instantiate(luz, newAgentPosition,luz.transform.rotation); //luz de prueba
                     lights[light.id].name=light.id;
                    }
                    //revisa el estado para modificar el color de la luz
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


    