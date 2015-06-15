import bpy
from mathutils import Vector
from . mn_utils import nameToPath as toPath

prefix = "AN "


def getIDKeys():
    scene = bpy.context.scene
    idKeys = getDefaultIDKeys()
    for item in scene.mn_settings.idKeys.keys:
        idKeys.append((item.name, item.type))
    return idKeys

def getDefaultIDKeys():
    return [("Initial Transforms", "Transforms")]
    
def removeIDKey(name):
    idKeys = bpy.context.scene.mn_settings.idKeys
    for item in idKeys.keys:
        if item.name == name:
            idKeys.remove(item)
    
def getIDType(name):
    for keyName, keyType in getIDKeys():
        if name == keyName: return keyType
    
def getIDTypeClass(type):
    return idTypes[type]
    
def getProp(object, name, default):
    return getattr(object, toPath(name), default)
def setProp(object, name, data):
    object[name] = data
def hasProp(object, name):
    return hasattr(object, toPath(name))
    
class NewIdKey(bpy.types.Operator):
    bl_idname = "mn.new_id_key"
    bl_label = "New ID Key"
    bl_description = "New Key"
    
    @classmethod
    def poll(cls, context):
        return not cls.nameExists(cls.getNewKeyData()[0])
    
    def execute(self, context):
        name, type = self.getNewKeyData()
        idKeys = context.scene.mn_settings.idKeys
        item = idKeys.keys.add()
        item.name = name
        item.type = type
        context.area.tag_redraw()
        return {'FINISHED'}    
        
    @classmethod
    def nameExists(cls, name):
        return getIDType(name) is not None
        
    @classmethod
    def getNewKeyData(cls):
        idKeySettings = bpy.context.scene.mn_settings.idKeys
        return idKeySettings.new_key_name, idKeySettings.new_key_type
    
class RemoveIDKey(bpy.types.Operator):
    bl_idname = "mn.remove_id_key"
    bl_label = "Remove ID Key"
    bl_description = "Remove this key"
    
    name = bpy.props.StringProperty()
    
    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        idKeys = context.scene.mn_settings.idKeys
        for i, item in enumerate(idKeys.keys):
            if item.name == self.name:
                idKeys.keys.remove(i)
        context.area.tag_redraw()
        return {'FINISHED'}
        
class CreateKeyOnObject(bpy.types.Operator):
    bl_idname = "mn.create_key_on_object"
    bl_label = "Create Key on Object"
    bl_description = ""
    
    name = bpy.props.StringProperty()
    type = bpy.props.StringProperty()
    objectName =  bpy.props.StringProperty()
    
    def execute(self, context):
        typeClass = getIDTypeClass(self.type)
        typeClass.create(bpy.data.objects.get(self.objectName), self.name)
        context.area.tag_redraw()
        return {'FINISHED'}        
    
    
class TransformsIDType:
    @classmethod
    def create(cls, object, name):
        cls.write(object, name, ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0)))

    @staticmethod
    def exists(object, name):
        return hasProp(object, prefix + name + "location") and \
               hasProp(object, prefix + name + "rotation") and \
               hasProp(object, prefix + name + "scale")

    @staticmethod
    def read(object, name):
        location = getProp(object, prefix + name + "location", (0, 0, 0))
        rotation = getProp(object, prefix + name + "rotation", (0, 0, 0))
        scale = getProp(object, prefix + name + "scale", (1, 1, 1))
        
        return Vector(location), Vector(rotation), Vector(scale)
        
    @staticmethod
    def write(object, name, data):
        setProp(object, prefix + name + "location", data[0])
        setProp(object, prefix + name + "rotation", data[1])
        setProp(object, prefix + name + "scale", data[2])
        
    @staticmethod
    def draw(layout, object, name):
        row = layout.row()
        
        col = row.column(align = True)
        col.label("Location")
        col.prop(object, toPath(prefix + name + "location"), text = "")
        
        col = row.column(align = True)
        col.label("Rotation")
        col.prop(object, toPath(prefix + name + "rotation"), text = "")
        
        col = row.column(align = True)
        col.label("Scale")
        col.prop(object, toPath(prefix + name + "scale"), text = "")
        
        
class FloatIDType:
    @classmethod
    def create(cls, object, name):
        cls.write(object, name, 1.0)

    @staticmethod
    def exists(object, name):
        return hasProp(object, prefix + name)

    @staticmethod
    def read(object, name):
        float = getProp(object, prefix + name, 0.0)
        return float
        
    @staticmethod
    def write(object, name, data):
        setProp(object, prefix + name, data)
        
    @staticmethod
    def draw(layout, object, name):
        layout.prop(object, toPath(prefix + name), text = "") 


class StringIDType:
    @classmethod
    def create(cls, object, name):
        cls.write(object, name, "")

    @staticmethod
    def exists(object, name):
        return hasProp(object, prefix + name)

    @staticmethod
    def read(object, name):
        string = getProp(object, prefix + name, "")
        return string
        
    @staticmethod
    def write(object, name, data):
        setProp(object, prefix + name, data)
        
    @staticmethod
    def draw(layout, object, name):
        layout.prop(object, toPath(prefix + name), text = "")        
        
        
idTypes = { "Transforms" : TransformsIDType,
            "Float" : FloatIDType,
            "String" : StringIDType }   
idTypeItems = [
    ("Transforms", "Transforms", "Contains 3 vectors for location, rotation and scale"),
    ("Float", "Float", "A single real number"),
    ("String", "String", "A text field")]     