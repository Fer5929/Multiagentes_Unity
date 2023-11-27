using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class move : MonoBehaviour
{
    [SerializeField] Vector3 displacement;
    [SerializeField] AXIS rotationAxiswheels;

    Mesh mesh;
    Mesh meshwheel1;
    Mesh meshwheel2;
    Mesh meshwheel3;
    Mesh meshwheel4;

    [SerializeField] GameObject wheel;
    [SerializeField] Vector3 posicion_wheel1;
    [SerializeField] Vector3 posicion_wheel2;
    [SerializeField] Vector3 posicion_wheel3;
    [SerializeField] Vector3 posicion_wheel4;
    [SerializeField] float angle_Right_wheels;
    [SerializeField] AXIS rotationAxis_Right_wheels;
    [SerializeField] float angle_Left_wheels;
    [SerializeField] AXIS rotationAxis_Left_wheels;
    [SerializeField] Vector3 scale;

    Vector3[] baseVertices;
    Vector3[] baseVerticeswheel1;
    Vector3[] baseVerticeswheel2;
    Vector3[] baseVerticeswheel3;
    Vector3[] baseVerticeswheel4;
    Vector3[] newVertices;
    Vector3[] newVerticeswheel1;
    Vector3[] newVerticeswheel2;
    Vector3[] newVerticeswheel3;
    Vector3[] newVerticeswheel4;
    float wheelvel;
    AXIS rotationAxis = AXIS.Y;
    float angle=0;
    // Start is called before the first frame update
    void Start()
    {
        GameObject wheel1=Instantiate(wheel, new Vector3(0, 0, 0), Quaternion.identity);
        GameObject wheel2=Instantiate(wheel, new Vector3(0, 0, 0), Quaternion.identity);
        GameObject wheel3=Instantiate(wheel, new Vector3(0, 0, 0), Quaternion.identity);
        GameObject wheel4=Instantiate(wheel, new Vector3(0, 0, 0), Quaternion.identity);

        mesh=GetComponentInChildren<MeshFilter>().mesh;
        meshwheel1=wheel1.GetComponentInChildren<MeshFilter>().mesh;
        meshwheel2=wheel2.GetComponentInChildren<MeshFilter>().mesh;
        meshwheel3=wheel3.GetComponentInChildren<MeshFilter>().mesh;
        meshwheel4=wheel4.GetComponentInChildren<MeshFilter>().mesh;

        baseVertices=mesh.vertices;
        baseVerticeswheel1 = meshwheel1.vertices;
        baseVerticeswheel2 = meshwheel2.vertices;
        baseVerticeswheel3 = meshwheel3.vertices;
        baseVerticeswheel4 = meshwheel4.vertices;


        //Allocate memory for the copu of the vertex list
        newVertices= new Vector3[baseVertices.Length];
        newVerticeswheel1= new Vector3[baseVerticeswheel1.Length];
        newVerticeswheel2= new Vector3[baseVerticeswheel2.Length];
        newVerticeswheel3= new Vector3[baseVerticeswheel3.Length];
        newVerticeswheel4= new Vector3[baseVerticeswheel4.Length];
        // Copy the coordinates
        for (int i=0; i<baseVertices.Length; i++){
            newVertices[i]=baseVertices[i];
        }
        
        for (int i=0; i<baseVerticeswheel1.Length; i++){
            newVerticeswheel1[i]=baseVerticeswheel1[i];
            newVerticeswheel2[i]=baseVerticeswheel2[i];
            newVerticeswheel3[i]=baseVerticeswheel3[i];
            newVerticeswheel4[i]=baseVerticeswheel4[i];
        }
        
        
    }

    // Update is called once per frame
    void Update()
    {
       
    }
    public void Dotransform(Vector3 prevPosition, Vector3 currPosition)
    {
        Matrix4x4 move = HW_Transforms.TranslationMat(currPosition.x,
                                              currPosition.y,
                                              currPosition.z);
            
        Matrix4x4 scalecar=HW_Transforms.ScaleMat(0.1810022f,
                                                    0.1810022f,
                                                    0.1810022f);
        /*Matrix4x4 moveOrigin=HW_Transforms.TranslationMat(-displacement.x,
                                                    -displacement.y,
                                                    -displacement.z);

        Matrix4x4 moveObject=HW_Transforms.TranslationMat(displacement.x,
                                                    displacement.y,
                                                    displacement.z);*/

        if (currPosition.z<prevPosition.z){
            angle=180;
        }
        if (currPosition.z>prevPosition.z){
            angle=-1;
        }
        else{
            if (currPosition.x>prevPosition.x){
            angle=90;
            }
            if (currPosition.x<prevPosition.x){
            angle=-90;
            }
        }
        //print(prevPosition.x);
        Matrix4x4 rotate=HW_Transforms.RotateMat(angle,rotationAxis);

        //Combine all matrix in single one
        Matrix4x4 composite =rotate*scalecar;
        Matrix4x4 composites = move*rotate*scalecar;

        //Multiply each vertex in the composite matrix
        for (int i=0; i<newVertices.Length; i++){
            Vector4 temp=new Vector4(baseVertices[i].x,
                                     baseVertices[i].y,
                                     baseVertices[i].z,
                                     1);
            newVertices[i]=composite * temp;
        }


        //remplace vertices in the mesh
        mesh.vertices=newVertices;
        mesh.RecalculateNormals();
        
        Matrix4x4 scales=HW_Transforms.ScaleMat(scale.x,scale.y,scale.z);
        Matrix4x4 rotateright=HW_Transforms.RotateMat(angle_Right_wheels, rotationAxis_Right_wheels);
        Matrix4x4 rotateleft=HW_Transforms.RotateMat(angle_Left_wheels, rotationAxis_Left_wheels);

        Matrix4x4 RightUp = HW_Transforms.TranslationMat(posicion_wheel3.x, posicion_wheel3.y, posicion_wheel3.z);
        Matrix4x4 RightBack = HW_Transforms.TranslationMat(posicion_wheel4.x, posicion_wheel4.y, posicion_wheel4.z);
        Matrix4x4 LeftUp = HW_Transforms.TranslationMat(posicion_wheel2.x, posicion_wheel2.y, posicion_wheel2.z);
        Matrix4x4 LeftBack = HW_Transforms.TranslationMat(posicion_wheel1.x, posicion_wheel1.y, posicion_wheel1.z);

        Matrix4x4 Right = scales * rotateright;
        Matrix4x4 Left = scales * rotateleft;
        wheelvel=currPosition.z*360;
        Matrix4x4 rotatewheel=HW_Transforms.RotateMat(wheelvel*Time.time,rotationAxiswheels);
        Matrix4x4 rotatewheel2=HW_Transforms.RotateMat(-wheelvel*Time.time,rotationAxiswheels);
        // Aplicar transformaciones de las ruedas en relación con el objeto principal
        
        Matrix4x4 RightUpcomposite =RightUp * Right;
        Matrix4x4 newcomposite =composites* RightUpcomposite*rotatewheel2;

        Matrix4x4 RightBackcomposite = RightBack * Right;
        Matrix4x4 newcomposite2 =composites* RightBackcomposite*rotatewheel2;

        Matrix4x4 LeftUpcomposite =LeftUp * Left;
        Matrix4x4 newcomposite3 =composites* LeftUpcomposite*rotatewheel;

        Matrix4x4 LeftBackcomposite =LeftBack * Left ;
        Matrix4x4 newcomposite4 =composites* LeftBackcomposite*rotatewheel;

        // Aplicar transformaciones a las coordenadas de las ruedas
        for (int i = 0; i < baseVerticeswheel1.Length; i++)
        {
            Vector4 temp = new Vector4(baseVerticeswheel1[i].x, baseVerticeswheel1[i].y, baseVerticeswheel1[i].z, 1);
            newVerticeswheel1[i] = newcomposite * temp;
        }
        for (int i = 0; i < baseVerticeswheel2.Length; i++)
        {
            Vector4 temp = new Vector4(baseVerticeswheel2[i].x, baseVerticeswheel2[i].y, baseVerticeswheel2[i].z, 1);
            newVerticeswheel2[i] = newcomposite2 * temp;
        }

        for (int i = 0; i < baseVerticeswheel3.Length; i++)
        {
            Vector4 temp = new Vector4(baseVerticeswheel3[i].x, baseVerticeswheel3[i].y, baseVerticeswheel3[i].z, 1);
            newVerticeswheel3[i] = newcomposite3 * temp;
        }

        for (int i = 0; i < baseVerticeswheel4.Length; i++)
        {
            Vector4 temp = new Vector4(baseVerticeswheel4[i].x, baseVerticeswheel4[i].y, baseVerticeswheel4[i].z, 1);
            newVerticeswheel4[i] = newcomposite4 * temp;
        }

        // Aplicar nuevas coordenadas a las mallas de las ruedas
        meshwheel1.vertices = newVerticeswheel1;
        meshwheel1.RecalculateNormals();

        meshwheel2.vertices = newVerticeswheel2;
        meshwheel2.RecalculateNormals();

        meshwheel3.vertices = newVerticeswheel3;
        meshwheel3.RecalculateNormals();

        meshwheel4.vertices = newVerticeswheel4;
        meshwheel4.RecalculateNormals();

    }
}
