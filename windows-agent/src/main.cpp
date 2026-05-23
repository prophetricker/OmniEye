#include <atomic>
#include <chrono>
#include <csignal>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <memory>
#include <string>
#include <thread>
#include <vector>

#include <camera/camera.h>
#include <camera/device_discovery.h>
#include <camera/photography_settings.h>

namespace {

std::atomic<bool> g_running{true};

void handleSignal(int) {
    g_running = false;
}

class FileStreamDelegate final : public ins_camera::StreamDelegate {
public:
    explicit FileStreamDelegate(std::filesystem::path output_dir)
        : output_dir_(std::move(output_dir)) {
        std::filesystem::create_directories(output_dir_);
    }

    void OnAudioData(const uint8_t*, size_t, int64_t) override {
    }

    void OnVideoData(const uint8_t* data, size_t size, int64_t timestamp, uint8_t, int stream_index = 0) override {
        if (stream_index != 0 || data == nullptr || size == 0) {
            return;
        }

        if (!stream_.is_open()) {
            const auto path = output_dir_ / "preview_stream_0.h264";
            stream_.open(path, std::ios::binary | std::ios::out);
            std::cout << "writing preview stream to " << path.string() << std::endl;
        }

        stream_.write(reinterpret_cast<const char*>(data), static_cast<std::streamsize>(size));
        last_video_timestamp_ = timestamp;
        bytes_written_ += size;
    }

    void OnGyroData(const std::vector<ins_camera::GyroData>&) override {
    }

    void OnExposureData(const ins_camera::ExposureData&) override {
    }

    size_t bytesWritten() const {
        return bytes_written_;
    }

    int64_t lastVideoTimestamp() const {
        return last_video_timestamp_;
    }

private:
    std::filesystem::path output_dir_;
    std::ofstream stream_;
    size_t bytes_written_{0};
    int64_t last_video_timestamp_{0};
};

struct Args {
    std::filesystem::path output_dir{"frames"};
    int seconds{30};
    bool verbose{false};
};

Args parseArgs(int argc, char** argv) {
    Args args;
    for (int i = 1; i < argc; ++i) {
        const std::string arg = argv[i];
        if (arg == "--output-dir" && i + 1 < argc) {
            args.output_dir = argv[++i];
        } else if (arg == "--seconds" && i + 1 < argc) {
            args.seconds = std::stoi(argv[++i]);
        } else if (arg == "--verbose") {
            args.verbose = true;
        } else if (arg == "--help") {
            std::cout << "Usage: omnieye_windows_agent [--output-dir frames] [--seconds 30] [--verbose]\n";
            std::exit(0);
        }
    }
    return args;
}

}  // namespace

int main(int argc, char** argv) {
    const auto args = parseArgs(argc, argv);
    std::signal(SIGINT, handleSignal);
    std::signal(SIGTERM, handleSignal);

    ins_camera::SetLogLevel(args.verbose ? ins_camera::LogLevel::VERBOSE : ins_camera::LogLevel::ERR);

    ins_camera::DeviceDiscovery discovery;
    auto devices = discovery.GetAvailableDevices();
    if (devices.empty()) {
        std::cerr << "No Insta360 camera found. Connect Windows to the X4 WiFi and retry." << std::endl;
        return 2;
    }

    for (const auto& device : devices) {
        std::cout << "camera: " << device.camera_name
                  << " serial=" << device.serial_number
                  << " fw=" << device.fw_version << std::endl;
    }

    auto camera = std::make_shared<ins_camera::Camera>(devices[0].info);
    if (!camera->Open()) {
        std::cerr << "Failed to open camera." << std::endl;
        discovery.FreeDeviceDescriptors(devices);
        return 3;
    }

    const auto camera_type = devices[0].camera_type;
    discovery.FreeDeviceDescriptors(devices);

    auto file_delegate = std::make_shared<FileStreamDelegate>(args.output_dir);
    std::shared_ptr<ins_camera::StreamDelegate> stream_delegate = file_delegate;
    camera->SetStreamDelegate(stream_delegate);

    if (camera_type >= ins_camera::CameraType::Insta360X4) {
        if (!camera->SetVideoSubMode(ins_camera::SubVideoMode::VIDEO_LIVEVIEW)) {
            std::cerr << "Failed to switch camera to live view mode." << std::endl;
            camera->Close();
            return 4;
        }

        ins_camera::RecordParams record_params;
        record_params.resolution = ins_camera::VideoResolution::RES_3840_1920P30;
        record_params.bitrate = 0;
        if (!camera->SetVideoCaptureParams(record_params, ins_camera::CameraFunctionMode::FUNCTION_MODE_LIVE_STREAM)) {
            std::cerr << "Failed to set live stream capture parameters." << std::endl;
            camera->Close();
            return 4;
        }
    }

    ins_camera::LiveStreamParam param;
    param.enable_audio = false;
    param.enable_video = true;
    param.enable_gyro = false;
    param.using_lrv = false;
    param.video_resolution = ins_camera::VideoResolution::RES_3840_1920P30;
    param.lrv_video_resulution = ins_camera::VideoResolution::RES_1440_720P30;
    param.video_bitrate = 1024 * 1024 / 2;
    param.lrv_video_bitrate = 1024 * 1024;

    if (!camera->StartLiveStreaming(param)) {
        std::cerr << "Failed to start live preview stream." << std::endl;
        camera->Close();
        return 4;
    }

    const auto start = std::chrono::steady_clock::now();
    while (g_running) {
        std::this_thread::sleep_for(std::chrono::seconds(1));
        const auto elapsed = std::chrono::duration_cast<std::chrono::seconds>(
            std::chrono::steady_clock::now() - start).count();
        std::cout << "elapsed=" << elapsed
                  << "s bytes=" << file_delegate->bytesWritten()
                  << " last_ts=" << file_delegate->lastVideoTimestamp() << std::endl;
        if (args.seconds > 0 && elapsed >= args.seconds) {
            break;
        }
    }

    camera->StopLiveStreaming();
    camera->Close();
    return 0;
}
