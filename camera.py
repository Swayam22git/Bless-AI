import os
import azure.ai.vision as sdk

service_options = sdk.VisionServiceOptions("https://cameratest01.cognitiveservices.azure.com/","254fa3e0f58d4133a566e3f565f170cb")

vision_source = sdk.VisionSource(
    url="https://learn.microsoft.com/azure/ai-services/computer-vision/media/quickstarts/presentation.png")

analysis_options = sdk.ImageAnalysisOptions()

analysis_options.features = (
    sdk.ImageAnalysisFeature.CAPTION |
    sdk.ImageAnalysisFeature.TEXT
)

analysis_options.language = "en"

analysis_options.gender_neutral_caption = True

image_analyzer = sdk.ImageAnalyzer(service_options, vision_source, analysis_options)

result = image_analyzer.analyze()

if result.reason == sdk.ImageAnalysisResultReason.ANALYZED:

    if result.caption is not None:
        print(" Caption:")
        print("   '{}', Confidence {:.4f}".format(result.caption.content, result.caption.confidence))

    if result.text is not None:
        print(" Text:")
        for line in result.text.lines:
            points_string = "{" + ", ".join([str(int(point)) for point in line.bounding_polygon]) + "}"
            print("   Line: '{}', Bounding polygon {}".format(line.content, points_string))
            for word in line.words:
                points_string = "{" + ", ".join([str(int(point)) for point in word.bounding_polygon]) + "}"
                print("     Word: '{}', Bounding polygon {}, Confidence {:.4f}"
                      .format(word.content, points_string, word.confidence))

else:

    error_details = sdk.ImageAnalysisErrorDetails.from_result(result)
    print(" Analysis failed.")
    print("   Error reason: {}".format(error_details.reason))
    print("   Error code: {}".format(error_details.error_code))
    print("   Error message: {}".format(error_details.message))

# import asyncio
# import io
# import os
# import sys
# import time
# import uuid
# import requests
# from urllib.parse import urlparse
# from io import BytesIO
# # To install this module, run:
# # python -m pip install Pillow
# from PIL import Image, ImageDraw
# from azure.cognitiveservices.vision.face import FaceClient
# from msrest.authentication import CognitiveServicesCredentials
# from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, QualityForRecognition


# # This key will serve all examples in this document.
# KEY = "254fa3e0f58d4133a566e3f565f170cb"

# # This endpoint will be used in all examples in this quickstart.
# ENDPOINT = "https://cameratest01.cognitiveservices.azure.com/"

# # Base url for the Verify and Facelist/Large Facelist operations
# IMAGE_BASE_URL = 'https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/'

# # Used in the Person Group Operations and Delete Person Group examples.
# # You can call list_person_groups to print a list of preexisting PersonGroups.
# # SOURCE_PERSON_GROUP_ID should be all lowercase and alphanumeric. For example, 'mygroupname' (dashes are OK).
# PERSON_GROUP_ID = str(uuid.uuid4()) # assign a random ID (or name it anything)

# # Used for the Delete Person Group example.
# TARGET_PERSON_GROUP_ID = str(uuid.uuid4()) # assign a random ID (or name it anything)

# # Create an authenticated FaceClient.
# face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

# '''
# Create the PersonGroup
# '''
# # Create empty Person Group. Person Group ID must be lower case, alphanumeric, and/or with '-', '_'.
# print('Person group:', PERSON_GROUP_ID)
# face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID, recognition_model='recognition_04')

# # Define woman friend
# woman = face_client.person_group_person.create(PERSON_GROUP_ID, name="Woman")
# # Define man friend
# man = face_client.person_group_person.create(PERSON_GROUP_ID, name="Man")
# # Define child friend
# child = face_client.person_group_person.create(PERSON_GROUP_ID, name="Child")

# '''
# Detect faces and register them to each person
# '''
# # Find all jpeg images of friends in working directory (TBD pull from web instead)
# woman_images = ["https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/Family1-Mom1.jpg", "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/Family1-Mom2.jpg"]
# man_images = ["https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/Family1-Dad1.jpg", "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/Family1-Dad2.jpg"]
# child_images = ["https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/Family1-Son1.jpg", "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/Family1-Son2.jpg"]

# # Add to woman person
# for image in woman_images:
#     # Check if the image is of sufficent quality for recognition.
#     sufficientQuality = True
#     detected_faces = face_client.face.detect_with_url(url=image, detection_model='detection_03', recognition_model='recognition_04', return_face_attributes=['qualityForRecognition'])
#     for face in detected_faces:
#         if face.face_attributes.quality_for_recognition != QualityForRecognition.high:
#             sufficientQuality = False
#             break
#         face_client.person_group_person.add_face_from_url(PERSON_GROUP_ID, woman.person_id, image)
#         print("face {} added to person {}".format(face.face_id, woman.person_id))

#     if not sufficientQuality: continue

# # Add to man person
# for image in man_images:
#     # Check if the image is of sufficent quality for recognition.
#     sufficientQuality = True
#     detected_faces = face_client.face.detect_with_url(url=image, detection_model='detection_03', recognition_model='recognition_04', return_face_attributes=['qualityForRecognition'])
#     for face in detected_faces:
#         if face.face_attributes.quality_for_recognition != QualityForRecognition.high:
#             sufficientQuality = False
#             break
#         face_client.person_group_person.add_face_from_url(PERSON_GROUP_ID, man.person_id, image)
#         print("face {} added to person {}".format(face.face_id, man.person_id))

#     if not sufficientQuality: continue

# # Add to child person
# for image in child_images:
#     # Check if the image is of sufficent quality for recognition.
#     sufficientQuality = True
#     detected_faces = face_client.face.detect_with_url(url=image, detection_model='detection_03', recognition_model='recognition_04', return_face_attributes=['qualityForRecognition'])
#     for face in detected_faces:
#         if face.face_attributes.quality_for_recognition != QualityForRecognition.high:
#             sufficientQuality = False
#             print("{} has insufficient quality".format(face))
#             break
#         face_client.person_group_person.add_face_from_url(PERSON_GROUP_ID, child.person_id, image)
#         print("face {} added to person {}".format(face.face_id, child.person_id))
#     if not sufficientQuality: continue


# '''
# Train PersonGroup
# '''
# # Train the person group
# print("pg resource is {}".format(PERSON_GROUP_ID))
# rawresponse = face_client.person_group.train(PERSON_GROUP_ID, raw= True)
# print(rawresponse)

# while (True):
#     training_status = face_client.person_group.get_training_status(PERSON_GROUP_ID)
#     print("Training status: {}.".format(training_status.status))
#     print()
#     if (training_status.status is TrainingStatusType.succeeded):
#         break
#     elif (training_status.status is TrainingStatusType.failed):
#         face_client.person_group.delete(person_group_id=PERSON_GROUP_ID)
#         sys.exit('Training the person group has failed.')
#     time.sleep(5)

# '''
# Identify a face against a defined PersonGroup
# '''
# # Group image for testing against
# test_image = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/identification1.jpg"

# print('Pausing for 10 seconds to avoid triggering rate limit on free account...')
# time.sleep (10)

# # Detect faces
# face_ids = []
# # We use detection model 3 to get better performance, recognition model 4 to support quality for recognition attribute.
# faces = face_client.face.detect_with_url(test_image, detection_model='detection_03', recognition_model='recognition_04', return_face_attributes=['qualityForRecognition'])
# for face in faces:
#     # Only take the face if it is of sufficient quality.
#     if face.face_attributes.quality_for_recognition == QualityForRecognition.high or face.face_attributes.quality_for_recognition == QualityForRecognition.medium:
#         face_ids.append(face.face_id)

# # Identify faces
# results = face_client.face.identify(face_ids, PERSON_GROUP_ID)
# print('Identifying faces in image')
# if not results:
#     print('No person identified in the person group')
# for identifiedFace in results:
#     if len(identifiedFace.candidates) > 0:
#         print('Person is identified for face ID {} in image, with a confidence of {}.'.format(identifiedFace.face_id, identifiedFace.candidates[0].confidence)) # Get topmost confidence score

#         # Verify faces
#         verify_result = face_client.face.verify_face_to_person(identifiedFace.face_id, identifiedFace.candidates[0].person_id, PERSON_GROUP_ID)
#         print('verification result: {}. confidence: {}'.format(verify_result.is_identical, verify_result.confidence))
#     else:
#         print('No person identified for face ID {} in image.'.format(identifiedFace.face_id))
 

# print()
# print('End of quickstart.')