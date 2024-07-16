PROMPT = """Analyze this image and give me the calories , protein, carbs and fat in the food in grams.
i want the response in a  format of
"{status:true,data={calories: ``kcal,protein: ``gm,carbs: ``gm,fat: ``gm},meal_contents='',information=''}".The information section should contain something interesting about the food or some medical advanatges of having this meal.meal_content should contain the side dishes and other items that are in the image. provide them as a array of items,eg:chicken, sauce .... If the image is not a food item or any other conveables,
the response should be {status:false}
    }}'
"""