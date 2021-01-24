import streamlit as st
st.set_page_config(page_icon="favicon.ico" )
from sklearn.externals import joblib
import pandas as pd
import numpy as np
import base64
from load_css import local_css
from PIL import Image,ImageOps
from keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background: url("data:image/png;base64,%s");
    background-size: cover;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

set_png_as_page_bg('image.png')
local_css("styles.css")
st.markdown("<div class='heading blue'><h1>FAUNUS</h1> </div>", unsafe_allow_html=True)
st.markdown("<div><h1 class='highlight blue'>Restore your Forest</h1> </div>", unsafe_allow_html=True)
st.title("")


rand_forest = joblib.load("random_forest_soil.pkl")
st.markdown("<div class='text blue'><h3><p>Choose the Soil Image</p></h3> </div>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["jpg",'png','jpeg'])

classes = {0:"Alluvial Soil",1:"Black Soil",2:"Clay Soil",3:"Red Soil"}
def model_predict(image):
    cnn_model= load_model('SoilNet_93_86.h5')
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = image.convert('RGB')
    size=(224,224)
    image=ImageOps.fit(image,size,Image.ANTIALIAS)
    
    image = np.asarray(image)
    image = image/255
    data[0] = image
    result = np.argmax(cnn_model.predict(data))
    prediction = classes[result]

    return(result)
    
    
    

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    prediction = model_predict(image)
    #st.write(prediction)

st.markdown("<div class='text blue'><h3><p>Enter top soil pH</p></h3> </div>", unsafe_allow_html=True)
pH = st.number_input("",key='h')
st.markdown("<div class='text blue'><h3><p>Enter drainage class</p></h3>  </div>", unsafe_allow_html=True)
drainage_class = st.number_input("",key='i')
st.markdown("<div class='text blue'><h3><p>Enter USDA topsoil texture</p></h3>  </div>", unsafe_allow_html=True)
topsoil_texture = st.number_input("",key='j')
st.markdown("<div class='text blue'><h3><p>Enter topsoil bulk density</p></h3>  </div>", unsafe_allow_html=True)
bulk_density = st.number_input("",key='k')

button=st.button('Check')
# channel = "<div class='text blue'><h3>Channel Treatment</h3><p>Channel treatments can used to modify sediment and water movement in stream channels, preventing flooding and debris torrents that threaten downstream communities and resources. These treatments often serve to slow water flow, allowing sediment to settle out, and then release sediments gradually through decay.</p> </div>"
# seeding = "<div class='text blue'><h3>Seeding</h3><p>The hillslope stabilization treatment can be done by aerial seeding of annual grasses. This activity has shown limited effectiveness, but remains the only method available to treat large areas in a short period of time and at a reasonably low cost per acre.</p> </div>"
# mulching = "<div class='text blue'><h3>Mulching</h3><p>Mulching is the most effective way to provide immediate ground cover to sensitive areas, but it also is relatively expensive and difficult to install. Also, a mixture of water, wood fiber mulch, seed and sometimes fertilizer known as hydromulch can be treated. This treatment provides protective benefits during the first year, even if seeds don’t germinate.</p> </div>"
# contour="<div class='text blue'><h3>Contour Log Felling</h3><p>Burned logs onsite can be used to create a mechanical barrier to water flow that also traps sediment and promotes infiltration. Dead trees are felled, limbed, cut to manageable size and placed on a contour perpendicular to the direction of the slope. Long tubes of plastic netting filled with straw, known as straw wattles, often are used in the same way as logs because they are easier and less hazardous to place.</p> </div>"
# silt="<div class='text blue'><h3>Silt Fences</h3><p>In areas where large-scale surface runoff with significant sedimentation is expected, fences hung with specially designed fabric can be erected.</p> </div>"
# tiling="<div class='text blue'><h3>Tilling and Scarification</h3><p>In areas where burn severity has created water repellent or hydrophobic soils, breaking up the hardened soil layer to increase infiltration and improve conditions for reseeding. This scarification can be done by hand on steep slopes using hand-rakes known as McLeods, or it can be conducted mechanically using all-terrain or other vehicles to drag a harrow across the ground.</p> </div>"

if(button):
    preds=pd.DataFrame({'pH':pH,"drainage_class":drainage_class,"topsoil_texture":topsoil_texture,"bulk_density":bulk_density},index=[0])
    type_ = rand_forest.predict(preds) 
    soils={0:"Alfisol",1:"Andisol",2:"Aridisol",3:"Entisol",4:"Histosol",5:"Inceptisol",6:"Mollisol",7:"Oxisol",8:"spodosol",9:"Ultisol",10:"Vertisol"}
    type_soil=type_
    if prediction ==0:
        alluvial="<div class='text blue'><h3>Alluvial Soil</h3><p>The alluvial soils vary in nature from sandy loam to clay. These soils are more loamy and clayey.The colour of the alluvial soils varies from the light grey to ash grey depending on the depth of the deposition, the texture of the materials, and the time taken for attaining maturity.These soils lack in nitrogen, phosphorus and humus. However, they are generally rich in potash and lime.The soil profile has no stratification.Alluvial soils are intensively cultivated.In certain areas, these soils are covered with unproductive wind-borne soil called Loess.Suitable Crops are: Wheat, rice, maize, sugarcane, pulses, oilseeds, fruits and vegetables, leguminous crops.</p></div>"
        st.markdown(alluvial,unsafe_allow_html=True)
    elif prediction ==1:
        black="<div class='text blue'><h3>Black Soil</h3><p>These soils are locally known as the ‘Regur Soil’ or the ‘Black Cotton Soil’. Internationally, these are known as ‘tropical chernozems’. These soils are famous for the cultivation of cotton.Black cotton soil (regur soil) is highly argillaceous i.e. clayey. It is deep and impermeable and thus has high water retention capacity.These soils are black in colour due to the presence of iron, aluminium compound.The soil depth varies from place to place. It is very thick in lowlands but very thin on highlands. These soils swell and become sticky when wet and develop deep wide cracks when dry. This helps in self-aeration, which leads to absorption of nitrogen from atmosphere. Thus, there occurs a kind of ‘self ploughing’. This aeration and oxidisation to deep levels contributes to maintenance of fertility of these soils.Chemically, the black soils are rich in lime, iron, magnesia and alumina. They also contain potash. But they lack in phosphorous, nitrogen and organic matter.Suitable Crops are: These soils are highly productive and well suited to the cultivation of cotton, pulses, millets, linseed, tobacco, sugar</p></div>"
        st.markdown(black,unsafe_allow_html=True)
    elif prediction ==2:
        clay="<div class='text blue'><h3>Clay Soil</h3><p>The word laterite has been derived from the Latin word ‘Later’ which means brick. These soils when wet are as soft as butter but become hard and cloddy on drying. Therefore, these are widely cut as bricks for use in house construction.Reddish brown in colour due to the presence of iron oxideWith rain, lime and silica are leached away, and soils rich in iron oxide and aluminium compound are left behind(thus the reddish brown colour). Also, humus content of the soil is removed fast by bacteria that thrives well in high temperature.These soils represent the end product of decomposition and are generally low in fertility.The pebbly crust is the important feature of laterites which is formed due to alteration of wet and dry periods.These soils are acidic in character due to leaching. Application of manures and fertilisers is required for making these soils fertile for cultivation.These soils are poor in organic matter, nitrogen, phosphate and calcium, while iron oxide and potash are in excess.Suitable crops are:Tea Plantations,cashewnuts,cane, vegetables and citrus fruits.</p></div>"
        st.markdown(clay,unsafe_allow_html=True)
    elif prediction ==3:
        red="<div class='text blue'><h3>Red Soil</h3><p>These are derived from granites, gneisses and other metamorphic rocks called Zonal Soils. These are formed under well-drained conditions.The soil develops a reddish colour due to a wide diffusion of iron in crystalline and metamorphic rocks.The soil texture varies from sand to clay and loamy.The fine-grained red soils are normally fertile, whereas coarse-grained soils found in dry upland areas are poor in fertility.They have a porous and friable structure.They are generally poor in nitrogen, phosphorous and humus.These soils are airy and need irrigation for cultivation.Intense leaching is a menace in these soil areas.Suitable Crops are: In places where irrigation facilities are available, the crops cultivated are wheat, cotton, pulses, tobacco, millets, oilseeds, potato, maize, groundnut and orchards.</p></div>"
        st.markdown(red,unsafe_allow_html=True)

    if type_soil[0][0]==1 :
        # st.markdown(channel,unsafe_allow_html=True)
        # st.markdown(seeding,unsafe_allow_html=True)
        # st.markdown(mulching,unsafe_allow_html=True)
        # st.markdown(contour,unsafe_allow_html=True)
        # st.markdown(silt,unsafe_allow_html=True)
        # st.markdown(tiling,unsafe_allow_html=True)
        alfisol="<div class='text blue'><h3>Alfisols</h3><p>Alfisols are moderately leached soils that have relatively high native fertility. These soils have formed primarily under forest and have a subsurface horizon in which clays have accumulated. Alfisols are found mostly in temperate humid and subhumid regions of the world.Alfisols occupy ~10.1% of the global ice-free land area. In the United States, they account for ~13.9% of the land area. Alfisols support about 17% of the world's population.The combination of generally favorable climate and high native fertility allows Alfisols to be productive soils for both agricultural and silvicultural use.Alfisols are divided into five suborders: Aqualfs, Cryalfs, Udalfs, Ustalfs, and Xeralfs.The trees favourable for this soil:FEVER TREE (VACHELLIA XANTHOPHLOEA), BAOBAB (ADANSONIA), SAUGAGE TREE (KIGELIA AFRICANA), QUIVER TREE (ALOE DICHOTOMA)</p></div>"
        st.markdown(alfisol,unsafe_allow_html=True)

    if (type_soil[0][1]==1) :
        pass
        # st.markdown(channel,unsafe_allow_html=True)
        # st.markdown(seeding,unsafe_allow_html=True)
        # st.markdown(mulching,unsafe_allow_html=True)
        # st.markdown(contour,unsafe_allow_html=True)
        # st.markdown(silt,unsafe_allow_html=True)
        # st.markdown(tiling,unsafe_allow_html=True)
        andisol="<div class='text blue'><h3>Andisols</h3><p>Andisols are soils that have formed in volcanic ash or other volcanic ejecta. They differ from those of other soil orders in that they typically are dominated by glass and short-range-order colloidal weathering products such as allophane, imogolite, and ferrihydrite (minerals). As a result, andisols have andic properties - unique chemical and physical properties that include high water-holding capacity and the ability to fix (and make unavailable to plants) large quantities of phosphorus.Globally, Andisols are the least extensive soil order and account for only about 1% of the ice-free land area. They occupy about 1.7% of the U.S. land area, including some productive forests in the Pacific Northwest region.Andisols are divided into eight suborders: Aquands, Gelands, Cryands, Torrands, Xerands, Vitrands, Ustands, and Udands.The trees favourable for this soil:Alerce (Fitzroya cupressoides), ciprés de las Guaitecas (Pilgerodendron uviferum),Chilean cypress (Austrocedrus chilensis),laurel (Laurelia sempervirens)</p> </div>"
        st.markdown(andisol,unsafe_allow_html=True)
    if type_soil[0][2]==1 :
        pass
        # st.markdown(channel,unsafe_allow_html=True)
        # st.markdown(seeding,unsafe_allow_html=True)
        # st.markdown(mulching,unsafe_allow_html=True)
        # st.markdown(contour,unsafe_allow_html=True)
        # st.markdown(silt,unsafe_allow_html=True)
        # st.markdown(tiling,unsafe_allow_html=True)
        aridisol="<div class='text blue'><h3>Aridisols</h3><p>Aridisols are calcium carbonate-containing soils of arid regions that exhibit at least some subsurface horizon development. They are characterized by being dry most of the year and having limited leaching. Aridisols contain subsurface horizons in which clays, calcium carbonate, silica, salts, and/or gypsum have accumulated. Materials such as soluble salts, gypsum, and calcium carbonate tend to be leached from soils of moister climates.Aridisols occupy about 12% of the Earth's ice-free land area and about 8.3% of the United States.Aridisols are used mainly for range, wildlife, and recreation. Because of the dry climate in which they are found, they are not used for agricultural production unless irrigation water is available.Aridisols are divided into seven suborders: Cryids, Salids, Durids, Gypsids, Argids, Calcids, and Cambids.Trees favourable for this soil::Calamagrostis epigejos(bush grass),Acacia ,Artemisia</p> </div>"
        st.markdown(aridisol,unsafe_allow_html=True)
    if type_soil[0][3]==1 :
        pass
        # st.markdown(channel,unsafe_allow_html=True)
        # st.markdown(seeding,unsafe_allow_html=True)
        # st.markdown(mulching,unsafe_allow_html=True)
        # st.markdown(contour,unsafe_allow_html=True)
        # st.markdown(silt,unsafe_allow_html=True)
        # st.markdown(tiling,unsafe_allow_html=True)
        entisol="<div class='text blue'><h3>Entisols</h3><p>Entisols are soils of recent origin. The central concept is that these soils developed in unconsolidated parent material with usually no genetic horizons except an A horizon. All soils that do not fit into one of the other 11 orders are entisols. Thus, they are characterized by great diversity, both in environmental setting and land use.Many entisols are found in steep, rocky settings. However, entisols of large river valleys and associated shore deposits provide cropland and habitat for millions of people worldwide.Globally, entisols are the most extensive of the soil orders, occupying about 18% of the Earth's ice-free land area. In the United States, entisols occupy about 12.3% of the land area.Entisols are divided into six suborders: Wassents, Aquents, Arents, Psamments, Fluvents, and Orthents.TREES favourable for this soil::Tsuga canadensis, Fagus grandifolia,Acer saccharum(Pinus resinosa), (Quercus alba),(Quercus velutina).</p> </div>"
        st.markdown(entisol,unsafe_allow_html=True)
    if type_soil[0][4]==1 :
        pass
        # st.markdown(channel,unsafe_allow_html=True)
        # st.markdown(seeding,unsafe_allow_html=True)
        # st.markdown(mulching,unsafe_allow_html=True)
        # st.markdown(contour,unsafe_allow_html=True)
        # st.markdown(silt,unsafe_allow_html=True)
        # st.markdown(tiling,unsafe_allow_html=True)
        histosol="<div class='text blue'><h3>Histosols</h3><p>Histosols are soils that are composed mainly of organic materials. They contain at least 20 to 30% organic matter by weight and are more than 40 cm thick. Bulk densities are quite low, often less than 0.3 grams per cubic centimeter.Most Histosols form in settings such as wetlands where restricted drainage inhibits the decomposition of plant and animal remains, allowing these organic materials to accumulate over time. As a result, Histosols are ecologically important because of the large quantities of carbon they contain. These soils occupy about 1.2% of the ice-free land area globally and about 1.6% of the United States.Histosols are often referred to as peats and mucks and have physical properties that restrict their use for engineering purposes. These include low weight-bearing capacity and subsidence when drained. They are mined for fuel and horticultural products.Histosols are divided into five suborders: Folists, Wassists, Fibrists, Saprists, and Hemists.TREES favourable for this soil::PIacea Obovata,Abies Sibiricam,Larix Sibirica,P.sylvestris</p> </div>"
        st.markdown(histosol,unsafe_allow_html=True)
    if type_soil[0][5]==1 :
        pass
        # st.markdown(channel,unsafe_allow_html=True)
        # st.markdown(seeding,unsafe_allow_html=True)
        # st.markdown(mulching,unsafe_allow_html=True)
        # st.markdown(contour,unsafe_allow_html=True)
        # st.markdown(silt,unsafe_allow_html=True)
        # st.markdown(tiling,unsafe_allow_html=True)
        inceptisol="<div class='text blue'><h3>Inceptisols</h3><p>Inceptisols are soils that exhibit minimal horizon development. They are more developed than Entisols but still lack the features that are characteristic of other soil orders.Inceptisols are widely distributed and occur under a wide range of ecological settings. They are often found on fairly steep slopes, young geomorphic surfaces, and resistant parent materials. Land use varies considerably with Inceptisols. A sizable percentage of Inceptisols are found in mountainous areas and are used for forestry, recreation, and watershed.Inceptisols occupy an estimated 15% of the global ice-free land area. Only the Entisols are more extensive. In the United States, they occupy about 9.7% of the land area. Inceptisols support about 20% of the world's population — the largest percentage of any of the soil orders.Inceptisols are divided into seven suborders: Aquepts, Anthrepts, Gelepts, Cryepts, Ustepts, Xerepts, and Udepts.TREES favourable for this soil::Hackberry,Willow,Silver maple ,Buttonbush,Ostrich fern</p> </div>"
        st.markdown(inceptisol,unsafe_allow_html=True)
    if type_soil[0][6]==1 :
        pass
        # st.markdown(channel,unsafe_allow_html=True)
        # st.markdown(seeding,unsafe_allow_html=True)
        # st.markdown(mulching,unsafe_allow_html=True)
        # st.markdown(contour,unsafe_allow_html=True)
        # st.markdown(silt,unsafe_allow_html=True)
        # st.markdown(tiling,unsafe_allow_html=True)
        mollisol="<div class='text blue'><h3>Mollisols</h3><p>Mollisols are the soils of grassland ecosystems. They are characterized by a thick, dark surface horizon. This fertile surface horizon, known as a mollic epipedon, results from the long-term addition of organic materials derived from plant roots.Mollisols primarily occur in the middle latitudes and are extensive in prairie regions such as the Great Plains of the United States. Globally, they occupy about 7.0% of the ice-free land area. In the United States, they are the most extensive soil order, accounting for about 21.5% of the land area.Mollisols are among some of the most important and productive agricultural soils in the world and are extensively used for this purpose.Mollisols are divided into eight suborders: Albolls, Aquolls, Rendolls, Gelolls, Cryolls, Xerolls, Ustolls, and Udolls.TREES favourable for this soil::Buffalo Grass,Sagebrush, Acacia,Eucalyptus sycamore</p> </div>"
        st.markdown(mollisol,unsafe_allow_html=True)
    if type_soil[0][7]==1 :
        pass
        # st.markdown(channel,unsafe_allow_html=True)
        # st.markdown(seeding,unsafe_allow_html=True)
        # st.markdown(mulching,unsafe_allow_html=True)
        # st.markdown(contour,unsafe_allow_html=True)
        # st.markdown(silt,unsafe_allow_html=True)
        # st.markdown(tiling,unsafe_allow_html=True)
        oxisol="<div class='text blue'><h3>Oxisols</h3><p>Oxisols  are very highly weathered soils that are found primarily in the intertropical regions of the world. These soils contain few weatherable minerals and are often rich in iron (Fe) and aluminum (Al) oxide minerals.Oxisols occupy about 7.5% of the global ice-free land area. In the United States, they only occupy about 0.02% of the land area and are restricted to Hawaii.Most of these soils are characterized by extremely low native fertility, resulting from very low nutrient reserves, high phosphorus retention by oxide minerals, and low cation exchange capacity (CEC). Most nutrients in Oxisol ecosystems are contained in the standing vegetation and decomposing plant material. Despite low fertility, Oxisols can be quite productive with inputs of lime and fertilizers.Oxisols are divided into five suborders: Aquox, Torrox, Ustox, Perox, and Udox.TREES favourable for this soil::Peltophorum dasyrrachis,Lagerstroemia angustifolia</p> </div>"
        st.markdown(oxisol,unsafe_allow_html=True)
    if type_soil[0][8]==1 :
        pass
        # st.markdown(channel,unsafe_allow_html=True)
        # st.markdown(seeding,unsafe_allow_html=True)
        # st.markdown(mulching,unsafe_allow_html=True)
        # st.markdown(contour,unsafe_allow_html=True)
        # st.markdown(silt,unsafe_allow_html=True)
        # st.markdown(tiling,unsafe_allow_html=True)
        spodosol="<div class='text blue'><h3>Spodosols</h3><p>Spodosols are acid soils characterized by a subsurface accumulation of humus that is complexed with Al and Fe. These photogenic soils typically form in coarse-textured parent material and have a light-colored E horizon overlying a reddish-brown spodic horizon. The process that forms these horizons is known as podzolization.Spodosols often occur under coniferous forest in cool, moist climates. Globally, they occupy ~4% of the ice-free land area. In the US, they occupy ~3.5% of the land area.Many Spodosols support forest. Because they are naturally infertile, Spodosols require additions of lime in order to be productive agriculturally.Spodosols are divided into 5 suborders: Aquods, Gelods, Cryods, Humods, and Orthods.TREES favourable for this soil::Black cherry,Quaking ,AspenHemlock,Sugar maple</p> </div>"
        st.markdown(spodosol,unsafe_allow_html=True)
    if type_soil[0][9]==1 :
        pass
        # st.markdown(channel,unsafe_allow_html=True)
        # st.markdown(seeding,unsafe_allow_html=True)
        # st.markdown(mulching,unsafe_allow_html=True)
        # st.markdown(contour,unsafe_allow_html=True)
        # st.markdown(silt,unsafe_allow_html=True)
        # st.markdown(tiling,unsafe_allow_html=True)  
        ultisol="<div class='text blue'><h3>Ultisols</h3><p>Ultisols are strongly leached and acidic forest soils with relatively low fertility. They are found primarily in humid temperate and tropical areas of the world, typically on older, stable landscapes. Intense weathering of primary minerals has occurred, and much calcium (Ca), magnesium (Mg), and potassium (K) has been leached from these soils. Ultisols have a subsurface horizon in which clays have accumulated, often with strong yellowish or reddish colors resulting from the presence of iron (Fe) oxides. The red clay soils of the southeastern United States are examples of Ultisols.Ultisols occupy about 8.1% of the global ice-free land area and support 18% of the world's population. They are the dominant soils of much of the southeastern United States and occupy about 9.2% of the total U.S. land area.Because of the favorable climate regimes in which they are typically found, Ultisols often support productive forests. The high acidity and relatively low quantities of plant-available Ca, Mg, and K associated with most Ultisols make them poorly suited for continuous agriculture without the use of fertilizer and lime. With these inputs, however, Ultisols can be very productive.Ultisols are divided into five suborders: Aquults, Humults, Udults, Ustults, and Xerults.TREES favourable for this soil::Tickweed,Spotted jewelweed,Mealcup sage ,Camassia</p> </div>"
        st.markdown(ultisol,unsafe_allow_html=True)   
    if type_soil[0][10]==1 :
        pass
        # st.markdown(channel,unsafe_allow_html=True)
        # st.markdown(seeding,unsafe_allow_html=True)
        # st.markdown(mulching,unsafe_allow_html=True)
        # st.markdown(contour,unsafe_allow_html=True)
        # st.markdown(silt,unsafe_allow_html=True)
        # st.markdown(tiling,unsafe_allow_html=True)
        vertisol="<div class='text blue'><h3>Vertisols</h3><p>Vertisols are clay-rich soils that shrink and swell with changes in moisture content. During dry periods, the soil volume shrinks and deep wide cracks form. The soil volume then expands as it wets up. This shrink/swell action creates serious engineering problems and generally prevents formation of distinct, well-developed horizons in these soils.Globally, Vertisols occupy about 2.4% of the ice-free land area. In the United States, they occupy about 2.0% of the land area and occur primarily in Texas.Vertisols are divided into six suborders: Aquerts, Cryerts, Xererts, Torrerts, Usterts, and Uderts.Trees favourable for this soil::Indian Mahogany (Swietania Mahogani),Ashoka Tree (Saraca Asoca),Gulmohar Tree (Delonix Regia)</p> </div>"
        st.markdown(vertisol,unsafe_allow_html=True)       

    st.markdown("<div class='text blue'><h2>Go to  <a href='https://shivanshu-sahoo.github.io/'>main website</a></h2></div>", unsafe_allow_html=True)