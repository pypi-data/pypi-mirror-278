from virtualbox import VirtualBox

VM_NAME = "test"
FOLDER = "/srv/vms/"
CPUS = 4
RAM = 2048
VRDE_PORT = 50004
HOST_NIC = "wlp4s0"
ISO = "../debian-12.5.0-amd64-netinst.iso"
HDD_SIZE = 10000

# Connect to VirtualBox
vbox = VirtualBox()

# Create VM
vm = vbox.create_vm(name=VM_NAME, ostype="Debian12_64", folder=FOLDER)

# Modify VM settings
vm.memory_size = RAM
vm.cpu_count = CPUS
vm.enable_vrdp = True
vm.vrdp_port = VRDE_PORT
vm.network_adapter(1).set_bridged_adapter(HOST_NIC)
vm.rtc_use_utc = True

# Create storage controller
sata_controller = vm.add_storage_controller(name="sata", adapter_type="sata", port_count=2, bootable=True)

# Create disk
disk = vm.create_hard_disk(name=f"{VM_NAME}.vmdk", size=HDD_SIZE, format="VMDK")
sata_controller.attach_device(disk, port=1)

# Attach ISO
iso = vm.attach_medium("sata", 2, medium_type="dvddrive", path=ISO)

# Start VM
vm.start(vm_type="headless")
