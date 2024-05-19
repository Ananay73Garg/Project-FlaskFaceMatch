#Import the modules.
import os
from flask import Flask,request,render_template
from deepface import DeepFace
import math
import statistics
	
#Start the App.
app = Flask(__name__)



	#Configure the Image folder.
app.config['UPLOAD_FOLDER'] = r'/Users/ananaygarg/Desktop/Code/project/images'
ax = []

#Route the app(Create its journey).
@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST' :
        file = request.files['file']
        imgname1 = file.filename
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)
	    
        file2 = request.files['file2']
        imgname2 = file2.filename
        path2 = os.path.join(app.config['UPLOAD_FOLDER'], file2.filename)
        file2.save(path2)
        img = path2
        img2 = path
        t = 0
        m = 1
        p = 0
        
        #The percentage function.
        def face_distance_to_conf(face_distance, face_match_threshold):
            if face_distance > face_match_threshold:
                range = (1.0 - face_match_threshold)
                linear_val = (1.0 - face_distance) / (range * 2.0)
                return linear_val
            
            else:
                range = face_match_threshold
                linear_val = 1.0 - (face_distance / (range * 2.0))
                return linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))


        #Start the analysis.
        
        try:
                    # models = ['VGG-Face','Facenet','OpenFace','ArcFace']
                    # metrics = ['cosine','euclidean','euclidean_l2']
                working  = ["VGG-Face","ArcFace"]
                for i in working:    
                    result = DeepFace.verify(img1_path=img,img2_path=img2,model_name=i)
                    face_distance = result['distance']
                    face_match_threshold = result['threshold']
                    confidence = face_distance_to_conf(face_distance, face_match_threshold)
                    percentage = round(confidence * 100, 2)
                    t+=percentage
                    
                    if result['verified']=='False' :
                        p+=1
                    else:
                        p-=1	
                        
                         
        except Exception as e :
            m = e 
        
        result1 = round(t/2,2)
        
        return render_template('result.html', result1=result1,result2 =m,result = p,img1 = img,img2 = img2,ax=ax)

    # for filex in os.listdir('/Users/ananaygarg/Desktop/Code/project/images'):
    #     if filex.endswith('.png') or filex.endswith('.jpeg'):
    #         os.remove(f'/Users/ananaygarg/Desktop/Code/project/images/{filex}')
    
    
    return render_template('upload.html')


#Run the app.    
if __name__ == "__main__":
    app.run(debug=True)
